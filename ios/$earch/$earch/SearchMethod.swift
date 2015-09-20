import Foundation

class SearchMethod {
    
    static func searchWithString(#query: String, completion:(SearchResponse) -> ()) {
        let escapedQuery = query.stringByAddingPercentEscapesUsingEncoding(NSUTF8StringEncoding)
        
        let url = NSURL(string: "http://192.168.88.13:9458/search?query=\(escapedQuery!)")
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