import Foundation

class News {
    
    let title: String
    let provider: NewsProvider
    let path: String
    var url: NSURL {
        get {
            return NSURL(string: self.path)!
        }
    }
    
    init(title: String, path: String) {
        self.title = title
        self.path = path
        self.provider = NewsProvider.providerForPath(self.path)
    }
    
}

enum NewsProvider {
    case ZERO_HEDGE
    case THE_STREET
    case ROUTERS
    case THE_TELEGRAPH
    case UNDEFINED
    
    static func providerForPath(url: String) -> NewsProvider {
        if url.hasPrefix("http://www.reuters") {
            return .ROUTERS;
        } else if url.hasPrefix("http://www.zerohedge") {
            return .ZERO_HEDGE;
        } else if url.hasPrefix("http://www.telegraph") {
            return .THE_TELEGRAPH;
        } else if url.hasPrefix("http://www.thestreet") {
            return .THE_STREET;
        } else {
            return .UNDEFINED;
        }
    }
}