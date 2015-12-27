//
//  TabbarViewController.swift
//  $earch
//
//  Created by Dominik Majda on 29.11.2015.
//  Copyright © 2015 BScThesis. All rights reserved.
//

import UIKit

class TabBarViewController: UITabBarController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        changeTabBarTintColor()
    }
    
    private func changeTabBarTintColor() {
        tabBar.tintColor = UIColor.whiteColor()
        let textColor = [NSForegroundColorAttributeName: UIColor.whiteColor()]
        UITabBarItem.appearance().setTitleTextAttributes(textColor, forState: UIControlState.Normal)
    }
    
}
