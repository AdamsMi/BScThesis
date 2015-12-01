import UIKit

class CategoriesViewController: UIViewController {

    @IBOutlet weak var categoriesCollectionView: UICollectionView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // MARK: - Customize view
    
    private func fadeOutAndReloadCollectionView() {
        UIView.transitionWithView(categoriesCollectionView,
            duration: 0.4,
            options: .TransitionCrossDissolve,
            animations: { () -> Void in
                self.categoriesCollectionView.alpha = 0.0
            }) { (result) -> Void in
                self.categoriesCollectionView.reloadData()
                self.fadeInCollectionView()
        }
    }
    
    private func fadeInCollectionView() {
        UIView.transitionWithView(categoriesCollectionView,
            duration: 0.4,
            options: .TransitionCrossDissolve,
            animations: { () -> Void in
                self.categoriesCollectionView.alpha = 1.0
            }, completion: nil)
    }


}

extension CategoriesViewController: UICollectionViewDelegate, UICollectionViewDataSource {
    
    func collectionView(collectionView: UICollectionView, didSelectItemAtIndexPath indexPath: NSIndexPath) {
        fadeOutAndReloadCollectionView()
    }
    
    func collectionView(collectionView: UICollectionView, cellForItemAtIndexPath indexPath: NSIndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCellWithReuseIdentifier(CategoryCollectionViewCell.cellName, forIndexPath: indexPath) as! CategoryCollectionViewCell
        return cell
    }
    
    func collectionView(collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 12
    }
    
}