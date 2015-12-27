import Foundation
import Alamofire
import SwiftyJSON

class SearchMethod {
    
    static func searchWithString(query query: String, completion:(SearchResponse) -> ()) {
        Alamofire.request(.GET, "http://localhost:9458/search", parameters: [
            "query" : query,
            "svd" : !LDASettings.ldaEnabled()])
            .responseJSON { response in
                
                if let json = response.result.value {
                    let searchResponse = SearchResponse(representation: JSON(json))
                    completion(searchResponse)
                }
        }
    }
    
    
    
    
}