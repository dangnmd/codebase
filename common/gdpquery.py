# pylint: disable=wildcard-import, invalid-name
from .gdpclient import *
from .pbdata import Base_pb2
from .pbdata import User_pb2
from .pbdata import IMUser_pb2
from .pbdata import IMBuddy_pb2
from .pbdata import Game_pb2
from .pbdata import bee_account_db_pb2
from .pbdata import FBAccount_pb2
from .pbdata import LogModel_pb2
from .pbdata import GxxModel_pb2

#Main

class GetUserAccount(GdpQuery):
	QUERY_NAME = 'GetUserAccount'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = User_pb2.UserAccount

class GetUserAccountOptional(GdpQuery):
	QUERY_NAME = 'GetUserAccount'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = User_pb2.UserAccount

class GetUserAccountLite(GdpQuery):
	QUERY_NAME = 'GetUserAccountLite'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = User_pb2.UserAccount

class GetUserProfile(GdpQuery):
	QUERY_NAME = 'GetUserProfile'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = User_pb2.UserProfile

class GetUserIdByName(GdpQuery):
	QUERY_NAME = 'GetUserIdByName'
	PARAMS_TYPE = str #username
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GetUserIdByEmail(GdpQuery):
	QUERY_NAME = 'GetUserIdByEmail'
	PARAMS_TYPE = str #username
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GetUserShell(GdpQuery):
	QUERY_NAME = 'GetUserShell'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = User_pb2.UserShell

class GetUserOtpSeedLite(GdpQuery):
	QUERY_NAME = 'GetUserOtpSeedLite'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = User_pb2.UserOtpSeed

class GetUserOtpSeed(GdpQuery):
	QUERY_NAME = 'GetUserOtpSeed'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = User_pb2.UserOtpSeed

class AddUserOtpSeed(GdpQuery):
	QUERY_NAME = 'AddUserOtpSeed'
	PARAMS_TYPE = User_pb2.UserOtpSeed

class GetOtpSeedConfig(GdpQuery):
	QUERY_NAME = 'GetOtpSeedConfig'
	PARAMS_TYPE = int  #spcode
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = User_pb2.OtpSpcodeConfig

class AddUserOtpSpcode(GdpQuery):
	QUERY_NAME = 'AddUserOtpSpcode'
	PARAMS_TYPE = (
		int,  #uid
		str,  #spcodes
		int,  #createtime
		int,  #updatetime
	)

class AddUserChangeOtpLog(GdpQuery):
	QUERY_NAME = 'AddUserChangeOtpLog'
	PARAMS_TYPE = (
		int,  #uid
		str,  #old_country_code
		str,  #new_country_code
		str,  #old_mobile
		str,  #new_mobile
		int,  #old_authenticator_enable
		int,  #new_authenticator_enable
		int,  #old_twostep_verify_enable
		int,  #new_twostep_verify_enable
		str,  #ip
		int,  #timestamp
	)

class IMGetUserInfo(GdpQuery):
	QUERY_NAME = 'IM.GetUserInfo'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = IMUser_pb2.UserInfo

class IMSetUserInfo(GdpQuery):
	QUERY_NAME = 'IM.SetUserInfo'
	PARAMS_TYPE = IMUser_pb2.UserInfo

class IMGetBuddies(GdpQuery):
	QUERY_NAME = 'IM.GetBuddies'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = IMBuddy_pb2.Buddy

class IMAddBuddy(GdpQuery):
	QUERY_NAME = 'IM.AddBuddy'
	PARAMS_TYPE = (
		int, #uid
		int, #buddyid
		int, #cateid
		int, #relation
		int, #createdate
	)

class IMAddBuddyPB(GdpQuery):
	QUERY_NAME = 'IM.AddBuddy:PB'
	PARAMS_TYPE = IMBuddy_pb2.Buddy

class IMRemoveBuddy(GdpQuery):
	QUERY_NAME = 'IM.RemoveBuddy'
	PARAMS_TYPE = (
		int, #uid
		int, #buddyid
	)

class GetGameStartLog(GdpQuery):
	QUERY_NAME = 'GetGameStartLog'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = Game_pb2.GameStartLog

class SetGameStartLog(GdpQuery):
	QUERY_NAME = 'SetGameStartLog'
	PARAMS_TYPE = Game_pb2.GameStartLog

class AddGameLoginLog(GdpQuery):
	QUERY_NAME = 'AddGameLoginLog'
	PARAMS_TYPE = Game_pb2.GameLoginLog

class GetOtpSpcode(GdpQuery):
	QUERY_NAME = 'GetOtpSpcode'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.String

class GetOtpToken(GdpQuery):
	QUERY_NAME = 'GetOtpToken'
	PARAMS_TYPE = int #token id
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = User_pb2.UserOtpToken

class AddFbConnect(GdpQuery):
	QUERY_NAME = 'AddFbConnect'
	PARAMS_TYPE = (
		int,  # uid
		int,  # fb_uid
		int,  # create_time
	)

class GetFbConnect(GdpQuery):
	QUERY_NAME = 'GetFbConnect'
	PARAMS_TYPE = int  # uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GetFbConnectEx(GdpQuery):
	QUERY_NAME = 'GetFbConnectEx'
	PARAMS_TYPE = int  # uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = FBAccount_pb2.FbConnect

class GetFbConnectByFbUid(GdpQuery):
	QUERY_NAME = 'GetFbConnectByFbUid'
	PARAMS_TYPE = int  # fb_uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.UInt

class RemoveFbConnect(GdpQuery):
	QUERY_NAME = 'RemoveFbConnect'
	PARAMS_TYPE = (
		int,  # uid
		int,  # fb_uid
	)

class AddFbUser(GdpQuery):
	QUERY_NAME = 'AddFbUser'
	PARAMS_TYPE = FBAccount_pb2.FbUser

class GetFbUser(GdpQuery):
	QUERY_NAME = 'GetFbUser'
	PARAMS_TYPE = (
		int,  # fb_uid
		int,  # fb_app_id
	)
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = FBAccount_pb2.FbUser

class GetFbUserMapping(GdpQuery):
	QUERY_NAME = 'GetFbUserMapping'
	PARAMS_TYPE = (
		int,  # fb_uid
		int,  # fb_app_id
	)
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = FBAccount_pb2.FbUserMapping

class AddFbUserMapping(GdpQuery):
	QUERY_NAME = 'AddFbUserMapping'
	PARAMS_TYPE = FBAccount_pb2.FbUserMapping

class IMAddFbBuddy(GdpQuery):
	QUERY_NAME = 'IM.AddFbBuddy'
	PARAMS_TYPE = (
		int,  # fid
		int,  # buddyid
	)

class AddFbConnectLog(GdpQuery):
	QUERY_NAME = 'AddFbConnectLog'
	PARAMS_TYPE = LogModel_pb2.FbConnectLog

class SetChangeUsernameQuota(GdpQuery):
	QUERY_NAME = 'SetChangeUsernameQuota'
	PARAMS_TYPE = (
		int,  # uid
		int,  # quota
		int,  # create_time
	)

class RemoveChangeUsernameQuota(GdpQuery):
	QUERY_NAME = 'RemoveChangeUsernameQuota'
	PARAMS_TYPE = int  # uid

class GetChangeUsernameQuota(GdpQuery):
	QUERY_NAME = 'GetChangeUsernameQuota'
	PARAMS_TYPE = int  # uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.UInt

class ExecuteModifyUsername(GdpQuery):
	QUERY_NAME = 'ExecuteModifyUsername'
	PARAMS_TYPE = (
		int,  # uid
		str,  # username
	)
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.UInt

class ExecuteRemoveUserEmail(GdpQuery):
	QUERY_NAME = 'ExecuteRemoveUserEmail'
	PARAMS_TYPE = (
		int, #uid
	)
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.UInt

class UpdateUserPassword(GdpQuery):
	QUERY_NAME = 'UpdateUserPassword'
	PARAMS_TYPE = (
		int,  # uid
		str,  # salt
		str,  # password
		int,  # password_s
	)

class ExecuteRegisterUser(GdpQuery):
	QUERY_NAME = 'ExecuteRegisterUser'
	PARAMS_TYPE = User_pb2.RegisterUserParams
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.UInt

class UpdateAndGetNextUid(GdpQuery):
	QUERY_NAME = 'UpdateAndGetNextUid'
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.UInt

class AddUserChangeUsernameLog(GdpQuery):
	QUERY_NAME = 'AddUserChangeUsernameLog'
	PARAMS_TYPE = LogModel_pb2.UserChangeUsername

class AddUserChangePasswordLog(GdpQuery):
	QUERY_NAME = 'AddUserChangePasswordLog'
	PARAMS_TYPE = LogModel_pb2.UserChangePassword

class AddUserRegisterSource(GdpQuery):
	QUERY_NAME = 'AddUserRegisterSource'
	PARAMS_TYPE = (
		int,  # uid
		str,  # source
	)

class GetMobileConnect(GdpQuery):
	QUERY_NAME = 'GetMobileConnect'
	PARAMS_TYPE = (
		str,  # mobile_no
	)
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = Base_pb2.UInt


# Attention: use this class instead of GetMobileBindings to get active bindings (status=1)
class GetMobileBindingsByStatus(GdpQuery):
	QUERY_NAME = 'GetMobileBindingsByStatus'
	PARAMS_TYPE = (
		str,  # country code
		str,  # mobile number
		int,  # status 1 is active, 0 inactive(bind and then unbind)
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GetMobileBindingsByUid(GdpQuery):
	QUERY_NAME = 'GetMobileBindingsByUid'
	PARAMS_TYPE = (
		int,  # uid
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = User_pb2.UserOtpMobileBinding

class AddMobileConnect(GdpQuery):
	QUERY_NAME = 'AddMobileConnect'
	PARAMS_TYPE = (
		int,  # uid
		str,  # mobile_no
		int,  # create_time
	)

class GetMobileBindings(GdpQuery):
	QUERY_NAME = 'GetMobileBindings'
	PARAMS_TYPE = (
		str,  # contry_code
		str,  # mobile_no
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = Base_pb2.UInt

class AddMobileBinding(GdpQuery):
	QUERY_NAME = 'AddMobileBinding'
	PARAMS_TYPE = User_pb2.UserOtpMobileBinding

class SetMobileBinding(GdpQuery):
	QUERY_NAME = 'SetMobileBinding'
	PARAMS_TYPE = User_pb2.UserOtpMobileBinding

class AddMobileConnectLog(GdpQuery):
	QUERY_NAME = 'AddMobileConnectLog'
	PARAMS_TYPE = (
		int,  # uid
		str,  # mobile_no
		int,  # create_time
	)

#BeeTalk

class BT_ACCOUNT_GetAccountByUserID(GdpQuery):
	QUERY_NAME = 'BT_ACCOUNT_GetAccountByUserID'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = bee_account_db_pb2.Account

class BT_ACCOUNT_GetAccountByAccount(GdpQuery):
	QUERY_NAME = 'BT_ACCOUNT_GetAccountByAccount'
	PARAMS_TYPE = str	#account
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = bee_account_db_pb2.Account

class BT_ACCOUNT_GetUserInfo(GdpQuery):
	QUERY_NAME = 'BT_ACCOUNT_GetUserInfo'
	PARAMS_TYPE = int #uid
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = bee_account_db_pb2.UserInfo

class BT_ACCOUNT_GetUserUniqueByUniqueID(GdpQuery):
	QUERY_NAME = 'BT_ACCOUNT_GetUserUniqueByUniqueID'
	PARAMS_TYPE = str #unique_id
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = bee_account_db_pb2.UserUniqueid

class BT_ACCOUNT_GetBindByUserIDAccountType(GdpQuery):
	QUERY_NAME = 'BT_ACCOUNT_GetBindByUserIDAccountType'
	PARAMS_TYPE = (
		int,	#uid
		str,	#account_type
	)
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = bee_account_db_pb2.Bind

class BT_BUDDY_GetUserBuddyList(GdpQuery):
	QUERY_NAME = 'BT_BUDDY_GetUserBuddyList'
	PARAMS_TYPE = (
		int,	#uid
		int,	#status
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = bee_account_db_pb2.UserBuddy

#GXX

class GxxGetUserInfo(GdpQuery):
	QUERY_NAME = 'Gxx.GetUserInfo'
	PARAMS_TYPE = (
		int,	#uid
	)
	RESULT_COUNT = GdpQuery.OPTIONAL_RESULT
	RESULT_TYPE = GxxModel_pb2.UserInfo

class GxxGetBuddyList(GdpQuery):
	QUERY_NAME = 'Gxx.GetBuddyList'
	PARAMS_TYPE = (
		int,	#uid
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = GxxModel_pb2.Buddy

class GxxGetBuddyUidList(GdpQuery):
	QUERY_NAME = 'Gxx.GetBuddyUidList'
	PARAMS_TYPE = (
		int,	#uid
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GxxAddUserToken(GdpQuery):
	QUERY_NAME = 'Gxx.AddUserToken'
	PARAMS_TYPE = GxxModel_pb2.UserToken
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GxxAddFollowee(GdpQuery):
	QUERY_NAME = 'Gxx.AddFollowee'
	PARAMS_TYPE = GxxModel_pb2.Followee

class GxxAddFollower(GdpQuery):
	QUERY_NAME = 'Gxx.AddFollower'
	PARAMS_TYPE = GxxModel_pb2.Follower

class GxxRemoveFollowee(GdpQuery):
	QUERY_NAME = 'Gxx.RemoveFollowee'
	PARAMS_TYPE = (
		int,	#uid
		int,	#followee_uid
	)

class GxxRemoveFollower(GdpQuery):
	QUERY_NAME = 'Gxx.RemoveFollower'
	PARAMS_TYPE = (
		int,	#uid
		int,	#follower_uid
	)

class GxxGetFollowerCount(GdpQuery):
	QUERY_NAME = 'Gxx.GetFollowerCount'
	PARAMS_TYPE = (
		int,	#uid
	)
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.UInt

class GxxGetFolloweeList(GdpQuery):
	QUERY_NAME = 'Gxx.GetFolloweeList'
	PARAMS_TYPE = (
		int,	#uid
	)
	RESULT_COUNT = GdpQuery.MULTI_RESULT
	RESULT_TYPE = GxxModel_pb2.Followee

class GxxGetFollowerExist(GdpQuery):
	QUERY_NAME = 'Gxx.GetFollowerExist'
	PARAMS_TYPE = (
		int,	#uid
		int,	#follower_uid
	)
	RESULT_COUNT = GdpQuery.SINGLE_RESULT
	RESULT_TYPE = Base_pb2.Bool

class UpdateUserOtpSeed(GdpQuery):
	QUERY_NAME = 'UpdateUserOtpSeed'
	PARAMS_TYPE = (
		User_pb2.UserOtpSeed
	)

class UpdateUserOtpSpcode(GdpQuery):
	QUERY_NAME = 'UpdateUserOtpSpcode'
	PARAMS_TYPE = (
		int,	#uid
		str,	#spcodes
		int,	#updatetime
	)

class UpdateMobileConnect(GdpQuery):
	QUERY_NAME = 'UpdateMobileConnect'
	PARAMS_TYPE = (
		int,	#uid
		str,	#mobile_no
	)

class UpdateMobileBindingsStatus(GdpQuery):
	QUERY_NAME = 'UpdateMobileBindingsStatus'
	PARAMS_TYPE = (
		int,	#uid
		str,	#country_code
		str,	#mobile_no
		int,	#status
	)

class RemoveUserOtpToken(GdpQuery):
	QUERY_NAME = 'RemoveUserOtpToken'
	PARAMS_TYPE = (
		int,	#uid
	)

class ExecuteModifyUserEmail(GdpQuery):
	QUERY_NAME = 'ExecuteModifyUserEmail'
	PARAMS_TYPE = (
		int,	#uid
		str,	#email
	)

class AddUserChangeEmailLog(GdpQuery):
	QUERY_NAME = 'AddUserChangeEmailLog'
	PARAMS_TYPE = (
		int,	#uid
		str,	#fromemail
		str,	#toemail
		int,	#verified
		str,	#ip
		int,	#timestamp
	)

class UpdateUserEmailVerified(GdpQuery):
	QUERY_NAME = 'UpdateUserEmailVerified'
	PARAMS_TYPE = (
		int,	#uid
		int,	#verified
	)

class UpdateUserStatus(GdpQuery):
	QUERY_NAME = 'UpdateUserStatus'
	PARAMS_TYPE = (
		int,	#uid
		int,	#status
	)

class UpdateUserAccCountry(GdpQuery):
	QUERY_NAME = 'UpdateUserAccCountry'
	PARAMS_TYPE = (
		int,	#uid
		str,	#acc_country
		int,	#update_time
	)
