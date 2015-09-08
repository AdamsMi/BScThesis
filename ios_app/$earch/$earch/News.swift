import Foundation

class News {
    
    let newsTitle: String
    let newsProvider: NewsProvider
    
    init(title: String, provider: NewsProvider) {
        self.newsTitle = title
        self.newsProvider = provider
    }
    
}

// This will be removed
class NewsGenerator {

    class func generateNews() -> [News] {
        
        let titles: [String] = [
            "FOMC Reaction - Stocks Rip, USD & Bond Yields Dip As Sept Rate-Hike Odds Drop To 40%",
            "WTI Collapses To A $40 Handle & What That Means For Earnings, In One Chart",
            "Nasdaq Drops Below 5,000 'Maginot' Line; S&P Unchanged In 2015",
            "One Word Defines This Era: Stagnation",
            "Corbyn lobbied Home Office to get extremist who condoned killing British soldiers into Britain"
        ]
        
        let providers: [NewsProvider] = [
            NewsProvider.ZERO_HEDGE,
            NewsProvider.ROUTERS,
            NewsProvider.THE_STREET,
            NewsProvider.THE_TELEGRAPH
        ]
        
        var randomNewsArray = [News]()
        
        for var i=0; i<30; i++ {
            var title = titles[Int(arc4random_uniform(5))]
            var provider = providers[Int(arc4random_uniform(4))]
            var news = News(title: title, provider: provider)
            randomNewsArray.append(news)
        }
        
        return randomNewsArray
    }
    
}

enum NewsProvider {
    case ZERO_HEDGE
    case THE_STREET
    case ROUTERS
    case THE_TELEGRAPH
}