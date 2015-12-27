//
//  SettingsViewController.swift
//  Search
//
//  Created by Dominik Majda on 17.12.2015.
//  Copyright © 2015 Adamczyk i Majda. All rights reserved.
//

import UIKit

class SettingsViewController: UIViewController {

    @IBOutlet weak var ldaEnabledSwitch: UISwitch!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        ldaEnabledSwitch.setOn(LDASettings.ldaEnabled(), animated: false)
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func switchChanges(sender: UISwitch) {
        
        LDASettings.setLDAsettings(sender.on)
        
    }
}
