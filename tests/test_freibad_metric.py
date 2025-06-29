
import unittest
import requests
import requests_mock
from freibad_metric import fetch_temperature

class TestFreibadMetric(unittest.TestCase):

    @requests_mock.Mocker()
    def test_fetch_temperature_success(self, m):
        """Test successful temperature fetching and parsing."""
        html_content = '<html><body>Aktuelle Wassertemperatur: 23,4 °C</body></html>'
        m.get("https://www.freibad-arnum.de/", text=html_content)
        temperature = fetch_temperature()
        self.assertEqual(temperature, 23.4)

    @requests_mock.Mocker()
    def test_fetch_temperature_not_found(self, m):
        """Test that a ValueError is raised when the temperature is not found."""
        html_content = '<html><body>Temperatur nicht verfügbar</body></html>'
        m.get("https://www.freibad-arnum.de/", text=html_content)
        with self.assertRaises(ValueError):
            fetch_temperature()

    @requests_mock.Mocker()
    def test_fetch_temperature_request_error(self, m):
        """Test that a requests.exceptions.HTTPError is raised on HTTP error."""
        m.get("https://www.freibad-arnum.de/", status_code=500)
        with self.assertRaises(requests.exceptions.HTTPError):
            fetch_temperature()

if __name__ == '__main__':
    unittest.main()
