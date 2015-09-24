import Foundation

class News {
    
    let newsTitle: String
    let newsProvider: NewsProvider
    let newsUrl: String
    
    init(title: String, url: String) {
        newsTitle = title
        newsUrl = url
        newsProvider = NewsProvider.urlProvider(url)
    }
    
}

enum NewsProvider {
    case ZERO_HEDGE
    case THE_STREET
    case ROUTERS
    case THE_TELEGRAPH
    case UNDEFINED
    
    static func urlProvider(url: String) -> NewsProvider {
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