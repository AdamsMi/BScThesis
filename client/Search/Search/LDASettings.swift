import Foundation

let LDA = "user"

class LDASettings {
    
    class func setLDAsettings(enabled: Bool) {
        let userDefaults = NSUserDefaults.standardUserDefaults()
        userDefaults.setBool(enabled, forKey: LDA)
        userDefaults.synchronize()
    }
    
    class func ldaEnabled() -> Bool {
        let userDefaults = NSUserDefaults.standardUserDefaults()
        return userDefaults.boolForKey(LDA)
    }
    
}
