@cd /D "%~dp0"
@FOR %%I IN ("*.proto") DO @(
	@echo %%I
	@protoc.exe --python_out=. "%%I"
)
@echo Build python over.
@pause