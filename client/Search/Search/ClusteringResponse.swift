import Foundation
import SwiftyJSON

class ClusteringResponse {

    let categories: [String: [String]]?
    let freqWords: [String: [String]]?
    let clusters: [String: Int]?
    
    init(representation: JSON) {
        
        categories = representation["res"].dictionaryObject as? [String: [String]]
        freqWords = representation["freqWords"].dictionaryObject as? [String: [String]]
        clusters = representation["clustering"].dictionaryObject as? [String: Int]
        
    }
    
}
