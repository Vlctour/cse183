import os
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

DEBUG = False
browser_options = webdriver.ChromeOptions()
if not DEBUG:
    browser_options.add_argument("--headless")

class StopGrading(Exception):
    pass

class Assignment(object):
    
    def __init__(self, path):
        self._comments = []
        fullpath = os.path.abspath(path)
        url = 'file://' + os.path.join(fullpath, 'assignment/index.html')
        print(f"Grading {url}")
        self.browser =  webdriver.Chrome(options=browser_options)
        self.goto(url)
        
    def goto(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(0.2)
        
    def refresh(self):
        self.browser.refresh()
        self.browser.implicitly_wait(0.2)
       
    def append_comment(self, points, comment):
        self._comments.append((points, comment))

    def step01(self):
        assert self.browser.find_element(By.TAG_NAME, 'html')
        return 0.5, "HTML is valid"

    def step02(self):
        table = self.browser.find_element(By.CSS_SELECTOR, 'table')
        bulma_classes = ['table', 'is-striped', 'is-fullwidth']
        assert set(bulma_classes).issubset(table.get_attribute('class').split()), "Table does not use Bulma CSS"
        return 0.5, "Table uses Bulma CSS" 
    
    def step03(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table tr')
        num_rows = len(rows)
        num_cols = max([len(r.find_elements(By.CSS_SELECTOR, 'td')) for r in rows])
        assert num_rows == 14 and num_cols == 3, f"Wrong number of rows and columns: {num_rows} rows, {num_cols} columns"
        return 0.5, "Correct number of rows and columns"

    def step04(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table tr')
        for i, r in enumerate(rows):
            assert r.get_attribute('class') == f'row-{i + 1}', f"Row {i + 1} does not have the correct class"
        return 1, "Row classes are correct"

    def step05(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table tr')
        content = (
            (1, "Income"),
            (7, "Payments, Credits, and Tax"),
            (13, "Refund"),
            (14, "Amount You Owe"),
        )
        for i, c in content:
            assert rows[i - 1].find_element(By.CSS_SELECTOR, 'td').text == c, f"First column header for row {i} is wrong"        
        return 0.5, "First column is correct"    

    def step06(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table tr')
        for i, r in enumerate(rows):
            cols = r.find_elements(By.CSS_SELECTOR, 'td')
            assert len(cols) >= 2, "Row with less than 2 columns"
            second_col = cols[-2].text
            assert second_col.startswith(str(i + 1) + " "), f"Row {i + 1} does not start with {i + 1}"
        return 1, "Second column is correct"
            
    def step07(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table tr')
        for i, r in enumerate(rows):
            cols = r.find_elements(By.CSS_SELECTOR, 'td')
            assert len(cols) > 0, "Row with less than 1 columns"
            col = cols[-1]
            input_field = col.find_element(By.CSS_SELECTOR, 'input')
            assert input_field, f"Row {i + 1} does not have an input field"
            assert input_field.get_attribute('name') == f'value-{i + 1}', f"Input field for row {i + 1} has wrong name"
        return 1, "Third column is correct"
        
    def step08(self):
        ro_fields = [4, 5, 6, 9, 10, 13, 14]
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table tr')
        for i, r in enumerate(rows):
            cols = r.find_elements(By.CSS_SELECTOR, 'td')
            assert len(cols) > 0, "Row with less than 1 columns"
            col = cols[-1]
            input_field = col.find_element(By.CSS_SELECTOR, 'input')
            (input_field.get_attribute('readonly') is not None) == (i + 1 in ro_fields), f"Input field for row {i + 1} read-only is wrong"
        return 0.5, "The required input fields are read-only."    

    def step09(self):
        test_values1 = (
            (('1', '2', '3'), 6),
            (('0', '3', '4'), 67))
        test_values2 = (
            (('10', '40', '80'), 130),
            (('0', '0', '00'), 8500))
        test_values = (test_values1, test_values2)
        for tv in test_values:
            self.refresh() # Otherwise, autocomplete breaks the test. 
            inp1 = self.browser.find_element(By.NAME, value='value-1')
            inp2 = self.browser.find_element(By.NAME, value='value-2')
            inp3 = self.browser.find_element(By.NAME, value='value-3')
            inp4 = self.browser.find_element(By.NAME, value='value-4')    
            for (v1, v2, v3), expected in tv:
                inp1.send_keys(v1)
                inp2.send_keys(v2)
                inp3.send_keys(v3)
                self.browser.implicitly_wait(0.1)
                value_1 = inp1.get_attribute('value')
                value_2 = inp2.get_attribute('value')
                value_3 = inp3.get_attribute('value')
                value_4 = inp4.get_attribute('value')
                assert float(value_4) == expected, f"Row 4 computation for inputs {value_1}, {value_2}, {value_3}, returned {value_4} instead of {expected}"
        return 1, "Row 4 computation correct for all test values"
        
    def step10(self):
        self.refresh()
        checkbox = self.browser.find_element(By.CSS_SELECTOR, '.row-5 input[type="checkbox"]')
        inp = self.browser.find_element(By.NAME, value='value-5')
        value_5 = float(inp.get_attribute('value'))
        assert value_5 == 13850, f"Field 5 value is {value_5} instead of 13850 when checkbox is not checked"
        checkbox.click()
        self.browser.implicitly_wait(0.1)
        value_5 = float(inp.get_attribute('value'))
        assert value_5 == 27700, f"Field 5 value is {value_5} instead of 27700 when checkbox is checked"
        return 1, "The checkbox on row 5 works."
        
    def step11(self):
        self.refresh()
        test_values = [
            [10000, 0],
            [30000, 1718],
            [60000, 5460.5],
            [100000, 14260.5],
            [200000, 38400],
            [500000, 142047],
            [1000000, 325207.5],
        ]
        for v, expected in test_values:
            field_1 = self.browser.find_element(By.NAME, value='value-1')
            field_14 = self.browser.find_element(By.NAME, value='value-14')
            field_1.clear()
            field_1.send_keys(str(v))
            value_14 = field_14.get_attribute('value')
            assert float(value_14) == expected, f"Tax computation for input {v}, returned {value_14} instead of {expected}"
        return 1, f"Tax computation correct for all test values"

    def step12(self):
        self.refresh()
        test_values = [
            (((1, 100200), (2, 500), (3, 1200), (7, 8000), (11, 1000)), 0, 7678.5,),
            (((1, 100200), (2, 500), (3, 1200), (7, 8000), (8, 500), (11, 1000)), 0, 7178.5,),
            (((1, 250000), (2, 1500), (3, 100), (7, 6000), (11, 3000)), 0, 52107.0,),
            (((1, 80000), (2, 5500), (3, 1700), (7, 5000), (11, 4000)), 0, 10444.5,),
            (((1, 80000), (2, 5500), (3, 1700), (7, 35000), (11, 4000)), 19555.5, 0,),
    ]
        for inps, out1, out2 in test_values:
            self.refresh() # Otherwise, autocomplete breaks the test.
            for i, v in inps:
                field = self.browser.find_element(By.NAME, value=f'value-{i}')
                field.clear()
                field.send_keys(str(v))
            field_13 = self.browser.find_element(By.NAME, value='value-13')            
            field_14 = self.browser.find_element(By.NAME, value='value-14')
            out_13 = float(field_13.get_attribute('value'))
            out_14 = float(field_14.get_attribute('value'))
            assert out_13 == out1, f"Row 13 computation for inputs {inps}, returned {out_13} instead of {out1}"
            assert out_14 == out2, f"Row 14 computation for inputs {inps}, returned {out_14} instead of {out2}"
        return 1.5, f"Tax computation correct for all test values"


    def grade(self):
        steps = [getattr(self, name) for name in dir(self) if name.startswith("step")]
        for step in steps:
            try:
                g, c = step()
                self.append_comment(g, step.__name__ + f": {g} point(s): {c}")
            except StopGrading:
                break
            except Exception as e:
                self.append_comment(0, f"Error in {step.__name__}: {e}")
        grade = 0
        for points, comment in self._comments:
            print("=" * 40)
            print(f"[{points} points]", comment)
            grade += points
        print("=" * 40)
        print(f"TOTAL GRADE {grade}")
        print("=" * 40)
        self.browser.quit()
        return grade

if __name__ == "__main__":
    tests = Assignment(".")
    tests.grade()
