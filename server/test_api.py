import unittest
import requests
import json

class TestCherrypyPrimer(unittest.TestCase):

        SITE_URL = 'http://localhost:51023' #'http://student04.cse.nd.edu:510XX' 
        DORMS_URL = SITE_URL + '/dorms/'
        RESET_URL = SITE_URL + '/reset/'

        def reset_data(self):
                d = {}
                r = requests.put(self.RESET_URL, data = json.dumps(d))

        def is_json(self, resp):
                try:
                        json.loads(resp)
                        return True
                except ValueError:
                        return False

        def test_dorm_get(self):
                self.reset_data()

                d_id = 11
                r = requests.get(self.DORMS_URL + str(d_id) + '/') 
                self.assertTrue(self.is_json(r.content.decode()))
                resp = json.loads(r.content.decode())

                self.assertEqual(resp['name'], 'Fisher')
                self.assertEqual(resp['year'], 1952)
                self.assertEqual(resp['gender'], 'Male')
                self.assertEqual(resp['quad'], 'South')
                self.assertEqual(resp['mascot'], 'Fishermen')

                d_id = 12
                r = requests.get(self.DORMS_URL + str(d_id) + '/') 
                self.assertTrue(self.is_json(r.content.decode()))
                resp = json.loads(r.content.decode())
                
                self.assertEqual(resp['name'], 'Flaherty')
                self.assertEqual(resp['year'], 2016)
                self.assertEqual(resp['gender'], 'Female')
                self.assertEqual(resp['quad'], 'Mod')
                self.assertEqual(resp['mascot'], 'Bears')

        def test_dorm_delete(self):
                self.reset_data()

                d_id = 1 # identifies first dorm (alumni)

                # delete data
                d = {}
                r = requests.delete(self.DORMS_URL + str(d_id) + '/', data = json.dumps(d))
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))
                self.assertEqual(resp['result'], 'success')

                # attempt to locate deleted data
                r = requests.get(self.DORMS_URL + str(d_id) + '/') 
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))
                self.assertEqual(resp['result'], 'error')

                # all other data should load successfully
                r = requests.get(self.DORMS_URL) # all other data should load successfully
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))
                self.assertEqual(resp['result'], 'success')

        def test_dorm_put(self):
                self.reset_data()
                r = requests.get(self.DORMS_URL)

                d_id = 33

                r = requests.get(self.DORMS_URL + str(d_id) + '/') # confirm get key 
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))
                self.assertEqual(resp['name'], 'Zahm')
                self.assertEqual(resp['year'], 1937)
                self.assertEqual(resp['gender'], 'Male')
                self.assertEqual(resp['quad'], 'North')
                self.assertEqual(resp['mascot'], 'Zahmbies')

                # replace zahm with sorin community in zahm :(

                d = {}
                d['name'] = 'Sorin Community in Zahm'
                d['year'] = 2021
                d['gender'] = 'Male'
                d['quad'] = 'North'
                d['mascot'] = 'The Resurrected'

                r = requests.put(self.DORMS_URL + str(d_id) + '/', data = json.dumps(d))
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))

                r = requests.get(self.DORMS_URL + str(d_id) + '/')
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))

                self.assertEqual(resp['name'], 'Sorin Community in Zahm')
                self.assertEqual(resp['year'], 2021)
                self.assertEqual(resp['gender'], 'Male')
                self.assertEqual(resp['quad'], 'North')
                self.assertEqual(resp['mascot'], 'The Resurrected')

                # create new dorm 

                new_id = 34
                d = {}
                d['name'] = 'McKenna'
                d['year'] = 2021
                d['gender'] = 'Male'
                d['quad'] = 'East'
                d['mascot'] = 'Eagles'
                
                r = requests.put(self.DORMS_URL + str(new_id) + '/', data = json.dumps(d))
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))

                r = requests.get(self.DORMS_URL + str(new_id) + '/')
                self.assertTrue(self.is_json(r.content.decode('utf-8')))
                resp = json.loads(r.content.decode('utf-8'))

                self.assertEqual(resp['name'], 'McKenna')
                self.assertEqual(resp['year'], 2021)
                self.assertEqual(resp['gender'], 'Male')
                self.assertEqual(resp['quad'], 'East')
                self.assertEqual(resp['mascot'], 'Eagles')

if __name__ == "__main__":
        unittest.main()
