import XMonad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ICCCMFocus
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.EwmhDesktops
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import System.IO
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.UrgencyHook
import XMonad.Hooks.SetWMName
import XMonad.Layout.Minimize
import XMonad.Layout.WindowNavigation
import XMonad.Layout.ToggleLayouts
import XMonad.Layout.IM as IM
import XMonad.Layout.PerWorkspace
import XMonad.Layout.Reflect
import XMonad.Layout.Grid
import Data.Ratio ((%))

import qualified Data.Map as M

-- Send applications to their dedicated Workspace
myManageHook = composeAll
                [ className =? "Skype"         --> doShift "4:skype"
                , className =? "Pidgin"        --> doShift "4:skype"
                , className =? "Gajim"         --> doShift "4:skype"
                , className =? "Thunderbird"   --> doShift "6:mail"
                , className =? "Unity-2d-panel" --> doIgnore
                ]


-- Name the workspaces                
myWorkspaces = ["1:dev","2:IDE","3:web","4:skype","5:media", "6:mail"] ++ map show [7..9]

-- Add new Keys
newKeys x = M.union (keys defaultConfig x) (M.fromList (myKeys x))

myKeys conf@(XConfig {XMonad.modMask = modm}) =
              [ 
              -- Minimize a window
                ((modm, xK_z),               withFocused minimizeWindow)
              , ((modm .|. shiftMask, xK_z), sendMessage RestoreNextMinimizedWin  )
              -- Window navigation with cursors
              , ((modm,                 xK_Right), sendMessage $ Go R)
              , ((modm,                 xK_Left ), sendMessage $ Go L)
              , ((modm,                 xK_Up   ), sendMessage $ Go U)
              , ((modm,                 xK_Down ), sendMessage $ Go D)
              , ((modm .|. controlMask, xK_Right), sendMessage $ Swap R)
              , ((modm .|. controlMask, xK_Left ), sendMessage $ Swap L)
              , ((modm .|. controlMask, xK_Up   ), sendMessage $ Swap U)
              , ((modm .|. controlMask, xK_Down ), sendMessage $ Swap D)           
              -- Togle Fullscreen
              , ((modm,                 xK_f    ), sendMessage ToggleLayout)
              , ((modm,                 xK_p        ), spawn "dmenu_run")
              ]

-- Define the default layout
rosterPidging = Role "buddy_list" 
rosterSkype = IM.And (ClassName "Skype")  (Title "ancechu - Skype™")
rosterGajim = Role "roster"

skypeLayout = IM.withIM (1%7) (IM.Or rosterGajim (IM.Or rosterPidging rosterSkype)) Grid
normalLayout = windowNavigation $ minimize $ avoidStruts $ onWorkspace "4:skype" skypeLayout $ layoutHook defaultConfig
myLayout = toggleLayouts (avoidStruts $ Full) normalLayout

-- Main executable 
main = do
    xmproc <- spawnPipe "xmobar /home/tcebrian/.xmobarrc"
    xmonad $ ewmh $ withUrgencyHook NoUrgencyHook $ defaultConfig
        { manageHook = manageDocks <+> myManageHook <+> manageHook defaultConfig 
        , keys = newKeys
        , workspaces = myWorkspaces 
        , layoutHook = myLayout
        , logHook = takeTopFocus >> dynamicLogWithPP xmobarPP
                        { ppOutput = hPutStrLn xmproc
                        , ppTitle = xmobarColor "green" "" . shorten 50
                        , ppUrgent = xmobarColor "yellow" "red" . xmobarStrip
                        }
        , modMask = mod4Mask     -- Rebind Mod to the Windows key
        , terminal = "terminator"
        , startupHook = setWMName "LG3D"
        } `additionalKeys`
        [ ((controlMask .|. shiftMask, xK_l), spawn "gnome-screensaver-command --lock")
        , ((controlMask, xK_Print), spawn "sleep 0.2; scrot -s")
        , ((0, xK_Print), spawn "scrot")
        ]
