import os
import glob
import simplejson
from prometheus_client import core


# More performance optimized version
class ExtendedMultiProcessCollector(object):
	def __init__(self, registry, path=os.environ.get('prometheus_multiproc_dir')):
		self._path = path
		if registry:
			registry.register(self)

	def collect(self):
		metrics = {}
		for f in glob.glob(os.path.join(self._path, '*.db')):
			parts = os.path.basename(f).split('_')
			typ = parts[0]
			d = core._MmapedDict(f)
			for key, value in d.read_all_values():
				# Because this loop occur many times (~100k) in production, using simplejson will make a large difference in Python 2.6
				metric_name, name, labelnames, labelvalues = simplejson.loads(key)
				if metric_name not in metrics:
					# Only init class when needed
					metrics[metric_name] = core.Metric(metric_name, 'Multiprocess metric', typ)
				metric = metrics[metric_name]

				if typ == 'gauge':
					pid = parts[2][:-3]
					metric._multiprocess_mode = parts[1]
					metric.add_sample(name, tuple(zip(labelnames, labelvalues)) + (('pid', pid),), value)
				else:
					# The duplicates and labels are fixed in the next for.
					metric.add_sample(name, tuple(zip(labelnames, labelvalues)), value)
			d.close()

		for metric in list(metrics.values()):
			samples = {}
			buckets = {}
			for name, labels, value in metric.samples:
				if metric.type == 'gauge':
					without_pid = tuple([l for l in labels if l[0] != 'pid'])
					if metric._multiprocess_mode == 'min':
						samples.setdefault((name, without_pid), value)
						if samples[(name, without_pid)] > value:
							samples[(name, without_pid)] = value
					elif metric._multiprocess_mode == 'max':
						samples.setdefault((name, without_pid), value)
						if samples[(name, without_pid)] < value:
							samples[(name, without_pid)] = value
					elif metric._multiprocess_mode == 'livesum':
						samples.setdefault((name, without_pid), 0.0)
						samples[(name, without_pid)] += value
					else:  # all/liveall
						samples[(name, labels)] = value
				elif metric.type == 'histogram':
					bucket = [float(l[1]) for l in labels if l[0] == 'le']
					if bucket:
						# _bucket
						without_le = tuple([l for l in labels if l[0] != 'le'])
						buckets.setdefault(without_le, {})
						buckets[without_le].setdefault(bucket[0], 0.0)
						buckets[without_le][bucket[0]] += value
					else:
						# _sum/_count
						samples.setdefault((name, labels), 0.0)
						samples[(name, labels)] += value
				else:
					# Counter and Summary.
					samples.setdefault((name, labels), 0.0)
					samples[(name, labels)] += value

			# Accumulate bucket values.
			if metric.type == 'histogram':
				for labels, values in list(buckets.items()):
					acc = 0.0
					for bucket, value in sorted(values.items()):
						acc += value
						samples[(metric.name + '_bucket', labels + (('le', core._floatToGoString(bucket)),))] = acc
					samples[(metric.name + '_count', labels)] = acc

			# Convert to correct sample format.
			metric.samples = [(name, dict(labels), value) for (name, labels), value in list(samples.items())]
		return list(metrics.values())
