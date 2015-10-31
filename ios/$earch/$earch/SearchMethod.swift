import Foundation

class SearchMethod {
    
    static func searchWithString(query query: String, completion:(SearchResponse) -> ()) {
        let escapedQuery = query.stringByAddingPercentEscapesUsingEncoding(NSUTF8StringEncoding)
        
        let url = NSURL(string: "http://10.22.110.255:9458/search?query=\(escapedQuery!)")
        let request = NSURLRequest(URL: url!)
        
        NSURLConnection.sendAsynchronousRequest(request,
            queue: NSOperationQueue.mainQueue()) {(response, data, error) in
                
            let jsonResult: NSDictionary = (try! NSJSONSerialization.JSONObjectWithData(data,
                options: NSJSONReadingOptions.MutableContainers)) as! NSDictionary
                
            print("\(jsonResult)")
                
            let response = SearchResponse(responseDict: jsonResult)
            completion(response)
        }
    }
    
    
}