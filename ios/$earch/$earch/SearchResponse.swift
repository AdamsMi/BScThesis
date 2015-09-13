import Foundation

class SearchResponse {
    
    let status: ResponseStatus
    var queryTime: Float
    var newsArray: Array<News>
    
    init(responseDict: NSDictionary) {
        newsArray = []
        queryTime = 0.0
        
        if let responseStatus: String = responseDict["status"] as? String {
            if responseStatus=="OK" {
                status = .OK
                queryTime = responseDict["query_time"] as! Float
                
                var newsArrayFromDict = responseDict["result"] as! NSArray
                for newsDict in newsArrayFromDict  {
                    let title = newsDict["title"] as! String
                    let url = newsDict["url"] as! String
                    newsArray.append(News(title: title, url: url))
                }
            } else {
                status = .FAILURE
            }
        } else {
            status = .FAILURE
        }
    }
    
    func isResponseOK() -> Bool {
        return status==ResponseStatus.OK
    }
    
}

enum ResponseStatus {
    case FAILURE
    case OK
}