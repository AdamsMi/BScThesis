import Foundation

class SearchMethod {
    
    static func searchWithString(#query: String, completion:(SearchResponse) -> ()) {
        
        let url = NSURL(string: "http://192.168.1.22:9458/search?query=\(query)")
        let request = NSURLRequest(URL: url!)
        
        NSURLConnection.sendAsynchronousRequest(request,
            queue: NSOperationQueue.mainQueue()) {(response, data, error) in
                
            var jsonResult: NSDictionary = NSJSONSerialization.JSONObjectWithData(data,
                options: NSJSONReadingOptions.MutableContainers, error: nil) as! NSDictionary
                
            println("\(jsonResult)")
                
            let response = SearchResponse(responseDict: jsonResult)
            completion(response)
        }
    }
    
    
}