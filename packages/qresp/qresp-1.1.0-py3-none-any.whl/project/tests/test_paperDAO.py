import unittest
from project.paperdao import PaperDAO,MongoDBConnection,Paper
import os
import json
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class TestPaperDAO(unittest.TestCase):
    def setUp(self):
        """
        Sets up database to test
        """
        MongoDBConnection.getDB(hostname='mongomock://localhost', port=int('27017'),
                                          username=None, password=None,
                                          dbname='mongoenginetest', collection='paper',
                                          isssl='No')
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'data.json')) as f:
            paperdata = json.load(f)
        paper = Paper(**paperdata)
        paper.save()

    def tearDown(self):
        """
        Sets up database to test
        """
        paper = Paper()
        paper.drop_collection()


    def test_getCollectionList(self):
        """
        Tests if all collections exist
        """
        dao = PaperDAO()
        allcollectionlist = dao.getCollectionList()
        self.assertTrue(list(allcollectionlist))

    def test_getPublicationList(self):
        """
        Tests for publications
        """
        dao = PaperDAO()
        allpublicationlist = dao.getPublicationList()
        self.assertTrue(list(allpublicationlist))

    def test_getAllPapers(self):
        """
        Tests for all papers
        """
        dao = PaperDAO()
        allpapers = dao.getAllPapers()
        self.assertTrue(list(allpapers))

    def test_getAllFilteredSearchObjects(self):
        """
        Tests for all search Objects
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects()
        self.assertTrue(list(allSearchObjects))

    def test_getFilteredPaperObjectsForAuthors(self):
        """
        Tests for all search Objects with name
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects(authorsList=['marco'])
        self.assertTrue(list(allSearchObjects))

    def test_getFilteredPaperObjectsForSearchWord(self):
        """
        Tests for all search Objects with name
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects(searchWord='photo')
        self.assertTrue(list(allSearchObjects))

    def test_getFilteredPaperObjectsForTitle(self):
        """
        Tests for all search Objects with name
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects(paperTitle='photo')
        self.assertTrue(list(allSearchObjects))

    def test_getFilteredPaperObjectsForTags(self):
        """
        Tests for all search Objects with name
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects(tags=['photo'])
        self.assertTrue(list(allSearchObjects))

    def test_getFilteredPaperObjectsForCollections(self):
        """
        Tests for all search Objects with name
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects(collectionList=['miccom'])
        self.assertTrue(list(allSearchObjects))

    def test_insertDOI(self):
        """
        Tests for insertion of DOI
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects()
        paper = dao.insertDOI(allSearchObjects[0]['_Search__id'],'123')
        self.assertEquals(1, paper)


    def test_getPaperDetails(self):
        """
        Tests Paper details given paper id
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects()
        paperDetails = dao.getPaperDetails(allSearchObjects[0]['_Search__id'])
        self.assertEquals(allSearchObjects[0]['_Search__id'], paperDetails['_PaperDetails__id'])


    def test_getWorkflowDetails(self):
        """
        Tests workflow details given paper id
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects()
        workflowdetails = dao.getWorkflowDetails(allSearchObjects[0]['_Search__id'])
        self.assertEquals(workflowdetails['paperTitle'],allSearchObjects[0]['_Search__title'])



    def test_getWorkflowForChartDetails(self):
        """
        Tests workflow details given chart id and paper id
        :return:
        """
        dao = PaperDAO()
        allSearchObjects = dao.getAllFilteredSearchObjects()
        paperDetails = dao.getPaperDetails(allSearchObjects[0]['_Search__id'])
        chartid = paperDetails['_PaperDetails__charts'][0].id
        workflowchartdetails = dao.getWorkflowForChartDetails(paperDetails['_PaperDetails__id'],chartid)
        self.assertEquals(workflowchartdetails['paperTitle'],allSearchObjects[0]['_Search__title'])

if __name__ == "__main__":
    unittest.main()