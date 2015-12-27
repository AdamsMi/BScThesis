import Foundation
import SwiftyJSON

class SearchResponse {
    
    let status: ResponseStatus
    var queryTime: Float?
    var newsArray: Array<News>
    
    init(representation: JSON) {
        newsArray = []
        queryTime = 0.0
        
        if let responseStatus = representation["status"].string {
            if responseStatus == "OK" {
                status = .OK
                queryTime = representation["query_time"].float
                
                let newsArrayFromDict = representation["result"].arrayValue
                for newsDict in newsArrayFromDict  {
                    let title = newsDict["title"].stringValue
                    let url = newsDict["url"].stringValue
                    newsArray.append(News(title: title, path: url))
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