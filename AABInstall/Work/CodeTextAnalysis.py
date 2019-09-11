#!use/bin/env python3
# -*- coding utf-8 -*-

import os
import io
import re
import json
import myopenpyxl

currentUsedLibrary = {}  # 代码中已使用的
unConfigLibrary = []  # 未使用配置文件 的信息库

basePath = 'E:\\WorkSpace\\WordGame\\WorkSpace\\NewWordSearch\\HiProject\\Assets\\'
pathArray = ['HiGameView\\', 'HiPlayView\\']
KeyConfigArray = [
    'GameConfig\\143\\Resources\\KeyConfigFile\\Text\\PlayUi\\en.txt', 'HiStyle\\Resources\\Skin1\\KeyConfigFile\\Text\\CommonUi\\en.txt']

bindKeys = ["ComingSoonUI_Text",
            "CommonUI_OkBtnText",
            "TopTipsUI_FontStyle",
            "TopTipsUI_FontStyle",
            "DailyRewardUI_DailyRewardText",
            "DailyRewardUI_GetText",
            "FaceBookLoadingUI_LoadingText",
            "FreeCoinsFromShopUI_Title",
            "FreeCoinsFromPlay_Text",
            "FreeCoinsFromShopUI_GoldCount",
            "FreeCoinsFromShopUI_WatchBtnText",
            "FreeCoinsFromPlay_ToggleInfo",
            "FreeCoinsFromShopUI_Title",
            "FreeCoinsFromPlay_Text",
            "FreeCoinsFromShopUI_GoldCount",
            "FreeCoinsFromShopUI_WatchBtnText",
            "FreeCoinsWatchUI_Title",
            "FreeCoinsWatchUI_AddNumber",
            "FreeCoinsWatchUI_Button",
            "Force_Agree",
            "Force_Detail",
            "CommonUI_OkBtnText",
            "PricayDetailUI_Cancel",
            "PricayDetailUI_Accept",
            "PrivacyUI_Title",
            "PrivacyUI_Detail",
            "PrivacyUI_Termas",
            "CommonUI_OkBtnText",
            "WebViewUI_Back",
            "CommonUI_OkBtnText",
            "LevelCompleteUI_MultiWordItemText",
            "PlayUI_BoundShowGridHint",
            "TopTipsUI_FontStyle",
            "TopTipsUI_FontStyle",
            "LevelCompleteUI_NextBtnText",
            "LoadingUI_LoadingText",
            "CommonUI_OkBtnText",
            "LogOutUi_LogOutText",
            "LogOutUI_ContentText",
            "CommonUI_YesText",
            "StproUI_Title",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "PackUI_LevelNumText",
            "RateUI_Title",
            "RateUI_AskTip",
            "RVTipUI_WatchVideoContent",
            "RVTipUI_WatchVideoBtn",
            "SettingsUI_SettingsText",
            "SettingsUI_HomeText",
            "SettingsUI_MapText",
            "SettingsUI_EmailUs",
            "SettingsUI_RestoreText",
            "SettingsUI_SoundText",
            "SettingsUI_MusicText",
            "SettingsUI_NotificationText",
            "SettleFailUI_ThemeText",
            "SettleFAilUI_ContentText",
            "SettleFailUI_RestartText",
            "SettleFailUI_ShuffleText",
            "TopTipsUI_FontStyle",
            "TopTipsUI_FontStyle",
            "RVTipUI_WatchVideoContent",
            "ShopUI_OneTimeOfferText",
            "ShopUI_GoldNum",
            "ShopUI_DollarText",
            "ShopUI_Discount",
            "ShopUI_ShopText",
            "ShopUI_OneTimeOfferText",
            "ShopUI_GoldNum",
            "ShopUI_DollarText",
            "ShopUI_Discount",
            "SpecialOfferUI_RateText",
            "SpecialOfferUI_TypeText",
            "SpecialOfferUI_DescribeText",
            "SpecialOfferUI_TitleText",
            "SpecialOfferUI_TypeText",
            "SpecialOfferUI_GoldCoinNum",
            "SpecialOfferUI_DescribeText",
            "SpecialOfferUI_RateText",
            "ShopUI_GiftDiscount",
            "TopTipsUI_FontStyle",
            "Turntable_RV_RewardItem",
            "Turntable_Discount_Price",
            "LevelCompleteUI_GoldCoinNum",
            "LevelCompleteUI_GoldCoinNum",
            "Turntable_RVAgain",
            "Turntable_RVAgain_TipText",
            "WaitUI_Loading",
            "PlayUI_SearchFreeCoinBtn",
            "PlayUI_FreeHint_Content",
            "FreeCoinsFromShopUI_WatchBtnText",
            "PlayUI_FreeHint_Title",
            "PlayUI_FreeHint_Des",
            "PlayUI_SearchFreeCoinBtn"
            ]
bindUtils = ["PlayUI_SearchItemCount",
             "PlayUI_SearchShowGridNotmal",
             "",
             "PlayUI_SearchItemCost",
             "PlayUI_SearchItemCost",
             "PlayUI_SearchShowGridNotmal",
             "",
             "PlayUI_SearchItemCost",
             "PlayUI_SearchItemCost"]
unBindPrefabText = ["AgainPlayCommingSoonUI---TitleText   CONGRATULATIONS",
                    "AgainPlayCommingSoonUI---Text   All levels completed!\nNew puzzles are coming soon!\nYou can restart the game from level 1.",
                    "AgainPlayCommingSoonUI---OkText   Level 1",
                    "AgainPlayJumpUI---TitleText   FRESH LEVELS",
                    "AgainPlayJumpUI---Text   New puzzles arrived! Tap the button to enjoy it!",
                    "AgainPlayJumpUI---OkText   GoTo",
                    "BackDoorUI---Text   X",
                    "BackDoorUI---Text   BackDoor",
                    "BackDoorUI---result   ",
                    "BackDoorUI---Placeholder   ",
                    "BackDoorUI---Text   ",
                    "BackDoorUI---Text   Login",
                    "BackDoorUI---PasswordText   Password:",
                    "BannerRemoveAdsUI---TitleText   REMOVE ADS",
                    "BannerRemoveAdsUI---Text   Buy now to no longer see ads.",
                    "BannerRemoveAdsUI---OkText   $3.99",
                    "CommonTopTipUI---Info   ",
                    "GoldCoinBtn---GoldCoinText   3000",
                    "HomeBtn---HomeText   Home",
                    "CommonTextTipUI---Text   ",
                    "CommonTextTipUI---Text   ",
                    "CommonTextTipUI---OkText   OK",
                    "DailyPuzzleSelectItem---Day   26",
                    "DailyPuzzleSelectUI---Title   DAILY",
                    "DailyPuzzleSelectUI---Title   ",
                    "DailyPuzzleSelectUI---Text   16/31",
                    "DailyPuzzleSelectUI---Text   50",
                    "DailyPuzzleSelectUI---Text   100",
                    "DailyPuzzleSelectUI---Text   200",
                    "DailyPuzzleSelectUI---Text   300",
                    "DailyPuzzleSelectUI---Count   ",
                    "DailyPuzzleSelectUI---Text   18",
                    "DailyPuzzleSelectUI---Next   NEXT",
                    "DailyPuzzleSelectUI---Cost   -25",
                    "DictionaryUI---textTitle   DICTIONARY",
                    "DictionaryUI---percent   4/7",
                    "DictionaryUI---wiktionary   Wiktionary",
                    "FeedBackUI---CloseText   Close",
                    "FeedBackUI---FeedBackText   FEEDBACk",
                    "FeedBackUI---ContactUsText   CONTACT US",
                    "FeedBackUI---ContentText   Thanks for your rating！\nIf you have any lssues and suggestions,\nplease contact us.Your feedback\nwill help us Improve our game!",
                    "ItemChangeToCoinUI---Text   Booster Flash has been replaced\nby a new booster Shuffle.\nYour existing Flash will be exchanged\nfor coins.",
                    "ItemChangeToCoinUI---AddNumber   +2800",
                    "CompleteWordItem---Word   ",
                    "GoldCoinIcon---GoldCoinNum   200",
                    "LevelCompleteBgImg---LevelCompleteText   LEVEL 25 COMPLETE",
                    "LevelMultiAnswerObj---ThemeText   uyjfhfhfgh",
                    "LevelSingleAnswerObj---Word   W",
                    "WordItem---Word   SHUZISs",
                    "LevelCompleteUI---Text   ",
                    "LevelCompleteUI---Text   ",
                    "LevelCompleteUI---ThemeTitle   thpooo",
                    "LevelCompleteUI---BarText   90/200",
                    "LevelCompleteUI---Text   ",
                    "LevelCompleteUI---Text   ",
                    "LevelCompleteUI---ThemeTitle   thpooo",
                    "LevelCompleteUIDaily---Text   OCTOBER 26 COMPLETE",
                    "LevelCompleteUIDaily---ThemeTitle   thpooo",
                    "LevelCompleteUIDaily---Text   26",
                    "LevelCompleteUINew---Text   ",
                    "LevelCompleteUINew---Text   ",
                    "LevelCompleteUINew---ThemeTitle   ",
                    "LevelCompleteUINew---Text   FeedBack",
                    "LevelCompleteUINew---Text   Translate",
                    "LevelCompleteUINew---BarText   90/200",
                    "LevelCompleteUINew---Text   New Theme\nunlocked!",
                    "LevelCompleteUINew---NextText   CLAIM",
                    "LevelCompleteUINew---coinValue   80",
                    "DialogFeedBackChooseOprationUI---tittle   -LEVEL REVIEW-",
                    "DialogFeedBackChooseOprationUI---Text   Words are too difficult/irregular or unmatched the theme-",
                    "DialogFeedBackChooseOprationUI---Text   Certain words missing in a level?",
                    "DialogFeedBackChooseOprationUI---Text   Other Problems.",
                    "DialogFeedBackJumpToContactUsUI---description   Any other suggestions please contact us!",
                    "DialogFeedBackJumpToContactUsUI---Text   LATER",
                    "DialogFeedBackJumpToContactUsUI---Text   CONTACT US",
                    "DialogFeedBackLevelReviewUI---tittle   -LEVEL REVIEW-",
                    "DialogFeedBackLevelReviewUI---description   -What do you think of this level?-",
                    "DialogFeedBackLevelReviewUI---Text   -Like-",
                    "DialogFeedBackLevelReviewUI---Text   -Dislike-",
                    "DialogFeedBackMissingWordUI---tittle   -MISSING WORD FEEDBACK-",
                    "DialogFeedBackMissingWordUI---description   -Multiple words should be separated with ", "-",
                    "DialogFeedBackMissingWordUI---Placeholder   ",
                    "DialogFeedBackMissingWordUI---Text   ",
                    "DialogFeedBackMissingWordUI---Text   SUBMIT",
                    "DialogFeedBackNotGoodWordUI---tittle   -LEVEL WORD FEEDBACK-",
                    "DialogFeedBackNotGoodWordUI---description   Here are all the words you found in this level. Please select all the difficult / irregular / unmatched words.",
                    "DialogFeedBackNotGoodWordUI---theme   ",
                    "DialogFeedBackNotGoodWordUI---Text   SUBMIT",
                    "DialogFeedBackNoWordsFoundUI---tittle   LEVEL WORD FEEDBACK",
                    "DialogFeedBackNoWordsFoundUI---description   You can only submit feedback on any level words you found!\nPlease play some levels first!",
                    "DialogFeedBackNoWordsFoundUI---Text   GOT IT",
                    "DialogFeedBackOtherProblemsUI---tittle   OTHERPROBLEMS",
                    "DialogFeedBackOtherProblemsUI---description   -Tap radio button to choose one or more.-",
                    "DialogFeedBackOtherProblemsUI---Text   SUBMIT",
                    "DialogFeedBackOtherProblemsUI---Text   This clue is boring or irregular",
                    "DialogFeedBackSuccessUI---description   ",
                    "DialogFeedBackSuccessUI---Text   -GOT IT-",
                    "Item---Count   200",
                    "MailNotificationUI---DescriptText   ",
                    "MailNotificationUI---Title   NEW MESSAGE",
                    "MailNotificationUI---OkText   ACCEPT",
                    "MusicMenuUI---Text (1)   MUSIC",
                    "MusicMenuUI---Gold   250",
                    "MusicSelectItem---MusicName   ",
                    "MusicSelectItem---Author   H.I.M",
                    "MusicSelectItem---PriceTxt   200",
                    "MusicTryUI---Text   Complete the October daily\nevent to earn this song. ",
                    "MusicTryUI---MusicName   Gone with the sin",
                    "MusicTryUI---Author   H.I.M",
                    "MusicTryUI---OkText   OK",
                    "SelectMusicItem---Text   ^",
                    "SelectMusicItem---Text   v",
                    "SelectMusicItem---Index   88",
                    "SelectMusicItem---Name   ",
                    "SelectMusicItem---Author   ",
                    "SelectMusicUI---Text   Close",
                    "NotificationUI---Title   REMIND ME",
                    "NotificationUI---DescriptText   Would you like to turn on\nNotifications for collecting\nDAILY GIFT?",
                    "NotificationUI---OkText   SURE",
                    "PackItem---LevelNumText   1",
                    "PurchaseFailUI---Text   Purchase failed.Please try again.",
                    "PurchaseWaitUI---Text   Loading…",
                    "SettingPackChapterItem---ChapterInfoText   New Text",
                    "SettingPackChapterItem---Info   Clear",
                    "SettingPackLevelItem---ChapterInfoText   ",
                    "SettingPackUI---Text (1)   CHAPTER",
                    "SettingPackUI---Gold   ",
                    "ContactUs---ContactUsText   CONTACT US",
                    "FaceBookLogin---FaceBookLoginText   FACEBOOK LOGIN",
                    "Help---HelpText   HELP",
                    "Music---MusicText   Music",
                    "Notification---NotificationText   Notification",
                    "Rate---RateText   RATE",
                    "Restore---RestoreText   RESTORE",
                    "SettingsUI---HomeText   SHOP",
                    "SettingsUI---HomeText   NO ADS",
                    "SettingsUI---ThemeText   THEMES",
                    "SettingsUI---PrivacyPolicyText   PRIVACY POLICY",
                    "SettingsUI---ManageMyDataText   MANAGE MY DATA",
                    "SettingsUI---Version   V1.0.1",
                    "Shop---RestoreText   SHOP",
                    "Sound---SoundText   Sound",
                    "SettleFailUseSuffleUI---TiltleText   SHUFFLE",
                    "SettleFailUseSuffleUI---ContentText   Use < color = red > SHUFFLE < /color > to rearrange\nthe titles.",
                    "SettleFailUseSuffleUI---FreeText   FREE",
                    "SettleFailUseSuffleUI---CoinNumText   200",
                    "ShopPackageDoubleTipUI---Text   2x",
                    "ShopPackageDoubleTipUI---Text (1)   Value",
                    "ShopPackageDoubleTipUI---Text   DOUBLE COIN SALE",
                    "ShopPackageDoubleTipUI---Text   ",
                    "ShopPackageDoubleTipUI---OkText   ",
                    "ShopPackageDoubleTipUI---Text   ",
                    "ShopPackageStarterTipUI---Text   STARTER KIT",
                    "ShopPackageStarterTipUI---Text   ",
                    "ShopPackageStarterTipUI---Text   0",
                    "ShopPackageStarterTipUI---Text   0",
                    "ShopPackageStarterTipUI---Text   0",
                    "ShopPackageStarterTipUI---OkText   ",
                    "ShopPackageStarterTipUI---Text   ",
                    "ShopContentUsUI---Text   YES",
                    "ShopContentUsUI---Text   NO",
                    "ShopItem---RecommendText   BEST",
                    "GiftTitle---Title   ONE TIME OFFER",
                    "NormalTitle---Title   DEALS",
                    "ShopNormalItem---RecommendText   BEST",
                    "ShopUI---ShopText   SHOP",
                    "ShopUI---Text   DEALS",
                    "ShopUI---Gold   250",
                    "SpecialOfferGradeUI---GoldCoinNum   5000",
                    "SpecialOfferGradeUI---GoldCoinNum   x140",
                    "SpecialOfferGradeUI---GoldCoinNum   x140",
                    "SpecialOfferGradeUI---GoldCoinNum   x140",
                    "SpecialOfferGradeUI---Time   05:30:04",
                    "StarTipUI---Title   STARS",
                    "StarTipUI---Text   100/100",
                    "StarTipUI---ContentText   Swipe in any direction to build words.\nFind all the words to complete",
                    "StartUI---LevelText   DAILY 60",
                    "StartUI---LevelText   DAILY",
                    "StartUI---Time   26",
                    "BgThemeItem---Text   Complete \nLevel100",
                    "BgThemeItem---Text   Zanga",
                    "BgThemeItem---Text   200",
                    "ThemeMenuUI---Text (1)   THEMES",
                    "ThemeMenuUI---Gold   250",
                    "TopTipsUI---GoldCoinText   500",
                    "TopTipsUI---LevelNumText   Level",
                    "VideoLoadingUI---Text   Loading…",
                    "DailyPuzzlePlayUI---Theme   26",
                    "DailyPuzzlePlayUI---Theme   ",
                    "DailyPuzzleWordItem---Normal    ",
                    "BoomItem---Text   New Text",
                    "PlayUI---ScoreText   40",
                    "PlayUI---Theme   ",
                    "WordItem---Normal    "]

noAdaptRE = re.compile(r'\.text *=')
PlayViewTextControllerStr = 'PlayViewTextController.Instance.GetTextString'
ResourceManagerStr = 'ResourceManager.TextDataPool'

allKeyConfigLibrary = {}  # 所有原有配置信息


def NotUsedLine(info):  # 是否是注释的行
    return info[0: 2] == '//'


def GetAllFilePath(root_path, file_list, dir_list):  # 获取所有文件和目录
    dir_or_files = os.listdir(root_path)  # 获取该目录下所有的文件名称和目录名称
    for dir_file in dir_or_files:  # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)  # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)  # 递归获取所有文件和目录的路径
            GetAllFilePath(dir_file_path, file_list, dir_list)
        else:
            if os.path.splitext(dir_file_path)[1] == '.cs':
                file_list.append(dir_file_path)


def AnalysisFile(filePath):  # 分析文件
    file = open(filePath, 'r', encoding='UTF-8')
    for line in file:
        tuple = re.findall(noAdaptRE, line)
        if tuple != None and len(tuple) > 0:
            info = line.strip()
            if not NotUsedLine(info[0: 2]):
                if PlayViewTextControllerStr in info:
                    info = info[info.index(
                        PlayViewTextControllerStr)+len(PlayViewTextControllerStr)+2:]
                    info = info[0: info.index(')')-1]
                    tempUseKey = info
                    if tempUseKey not in bindKeys:
                        bindKeys.append(tempUseKey)
                elif ResourceManagerStr in info:
                    info = info[info.index(
                        ResourceManagerStr)+len(ResourceManagerStr)+2:]
                    info = info[0: info.index(']')-1]
                    tempUseKey = info
                    if tempUseKey not in bindUtils:
                        bindUtils.append(tempUseKey)
                else:
                    if ('=""' not in info) and ('= ""' not in info):
                        unConfigLibrary.append(
                            os.path.basename(filePath) + '---' + info)
    file.close()


def GetKeyConfigData():  # 获取原有配置文件
    global allKeyConfigLibrary
    allKeyConfigLibrary = {}
    for tempDir in KeyConfigArray:
        file = open(basePath+tempDir, 'r', encoding='UTF-8')
        configInfo = file.read()
        file.close()
        tempData = json.loads(configInfo)
        for dic in tempData:
            allKeyConfigLibrary[dic['Key']] = dic['Value']


def PushDataToUsedLibrary():  # 处理已使用数据
    global currentUsedLibrary
    for key in bindKeys:
        if (key not in currentUsedLibrary) and (key in allKeyConfigLibrary):
            dic = {}
            dic['oldKey'] = key
            dic['info'] = allKeyConfigLibrary[key]
            currentUsedLibrary[key] = dic

    for key in bindUtils:
        if (key not in currentUsedLibrary) and (key in allKeyConfigLibrary):
            dic = {}
            dic['oldKey'] = key
            dic['info'] = allKeyConfigLibrary[key]
            currentUsedLibrary[key] = dic


def OutPutResult(filePath):  # 输出分析结果
    global currentUsedLibrary

    tempName = filePath + "config.xlsx"
    wb = myopenpyxl.CreateNewXlsx(tempName)
    ws = myopenpyxl.GetNowActiveSheet(wb)

    num = 1
    for dic in currentUsedLibrary.values():
        index = str(num)
        myopenpyxl.SetTargetCellPos(ws, 'A' + index, dic['oldKey'])
        myopenpyxl.SetTargetCellPos(ws, 'B' + index, dic['info'])
        num += 1

    num = 1
    for data in unConfigLibrary:
        index = str(num)
        myopenpyxl.SetTargetCellPos(ws, 'C' + index, data)
        num += 1

    num = 1
    for data in unBindPrefabText:
        index = str(num)
        myopenpyxl.SetTargetCellPos(ws, 'D' + index, data)
        num += 1

    myopenpyxl.WriteXlsx(wb, tempName)


def Analysis():  # 处理数据
    fileList = []
    dirList = []
    for tempDir in pathArray:
        GetAllFilePath(basePath+tempDir, fileList, dirList)
    for tempFilePath in fileList:
        AnalysisFile(tempFilePath)
    GetKeyConfigData()
    PushDataToUsedLibrary()
    OutPutResult(input('please input package path: \n'))


Analysis()
