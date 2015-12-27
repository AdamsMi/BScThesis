import Foundation
import Alamofire
import SwiftyJSON

class ClusteringMethod {
    
    
    static func initialClustering(completion:(ClusteringResponse) -> ()) {
        Alamofire.request(.GET, "http://localhost:9458/topic")
            .responseJSON { response in
                
                if let json = response.result.value {
                    
                    let clusteringResponse = ClusteringResponse(representation: JSON(json))
                    completion(clusteringResponse)
                    
                }
        }
    }
    
    static func clusterForPath(clusterId: [String], completion:(ClusteringResponse) -> ()) {
        
        let pathString = clusterId.joinWithSeparator("_")
        
        Alamofire.request(.GET, "http://localhost:9458/topic", parameters: ["id" : pathString])
            .responseJSON { response in
                
                if let json = response.result.value {
                    
                    let clusteringResponse = ClusteringResponse(representation: JSON(json))
                    completion(clusteringResponse)
                    
                }
            }
        
    }
    
    
    static func articlesForPath(clusterId: [String], completion:(SearchResponse) -> ()) {
        
        let pathString = clusterId.joinWithSeparator("_")
        
        Alamofire.request(.GET, "http://localhost:9458/articles", parameters: ["id" : pathString])
            .responseJSON { response in
                
                
                if let json = response.result.value {
                    let clusteringResponse = SearchResponse(representation: JSON(json))
                    completion(clusteringResponse)
                }
        }
        
    }
    
    
}