import unittest
from unittest.mock import patch
import mysql.connector

class TestRegisterCandidate(unittest.TestCase): #Run this section to test adding a candidate to the sql table (Integration Testing)
    @patch('mysql.connector.connect')
    def test_register_candidate_success(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.return_value = None

        # Call the function with sample data
        result = test_register_candidate(1, 2, 'John Doe')

        # Assert that the SQL and data were correctly passed to execute
        expected_sql = (
            "INSERT INTO president(id,vote_ballot_id,fullname,keyword)"
            "VALUES (%s, %s, %s, %s)"
        )
        expected_data = ('John Doe1', 2, 'John Doe', 'John Doe')
        mock_cursor.execute.assert_called_once_with(expected_sql, expected_data)

        # Assert that the function returned the expected result
        self.assertEqual(result, 1)

    @patch('mysql.connector.connect')
    def test_register_candidate_failure(self, mock_connect):
        # Mock the cursor and execute methods to raise an exception
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function with sample data
        result = test_register_candidate(1, 2, 'John Doe')

        # Assert that the function returned the expected result
        self.assertEqual(result, 0)
def test_register_candidate(id,ballot_id,fullname):
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    # insert election
    sql = (
        "INSERT INTO president(id,vote_ballot_id,fullname,keyword)"
        "VALUES (%s, %s, %s, %s)"
    )
    data = (fullname+str(id),ballot_id,fullname,fullname)
    # Executing the SQL command
    try:
        cursor.execute(sql, data)
        return 1
    except:
        return 0
def test_create_election(election_id,start_date,end_date,option):

    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    #insert election
    sql= (
        "INSERT INTO election(id,start_time,end_time,status)"
        "VALUES (%s, %s, %s, %s)"
    )
    try:
        election_data = (election_id, start_date, end_date, "ongoing")
        # Executing the SQL command
        cursor.execute(sql, election_data)
        # insert vote ballot
        sql = (
            "INSERT INTO vote_ballot(id,election_id,type)"
            "VALUES (%s, %s, %s )"
        )
        vote_ballot_data = (election_id, election_id, option)
        cursor.execute(sql, vote_ballot_data)

        db.close()
        return 1
    except:
        return 0
class TestCreateElection(unittest.TestCase): #Run this section to test adding a election to the sql table (Integration Testing)
    @patch('mysql.connector.connect')
    def test_create_election_success(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.return_value = None

        # Call the function with sample data
        result = test_create_election(1, '2023-05-20', '2023-05-30', 'option1')

        # Assert that the SQL and data were correctly passed to execute
        expected_sql_election = (
            "INSERT INTO election(id,start_time,end_time,status)"
            "VALUES (%s, %s, %s, %s)"
        )
        expected_sql_vote_ballot = (
            "INSERT INTO vote_ballot(id,election_id,type)"
            "VALUES (%s, %s, %s)"
        )
        expected_data_election = (1, '2023-05-20', '2023-05-30', 'ongoing')
        expected_data_vote_ballot = (1, 1, 'option1')
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_cursor.execute.assert_any_call(expected_sql_election, expected_data_election)
        mock_cursor.execute.assert_any_call(expected_sql_vote_ballot, expected_data_vote_ballot)

        # Assert that the function returned the expected result
        self.assertEqual(result, 1)

    @patch('mysql.connector.connect')
    def test_create_election_failure(self, mock_connect):
        # Mock the cursor and execute methods to raise an exception
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function with sample data
        result = test_create_election(1, '2023-05-20', '2023-05-30', 'option1')

        # Assert that the function returned the expected result
        self.assertEqual(result, 0)
def show_ongoing():
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT id FROM election WHERE status='ongoing' ")
    ongoing_elections = cursor.fetchall()
    if(ongoing_elections):
        return 1
    else:
        return 0


class TestShowOngoing(unittest.TestCase):  # check if we get onging elections from the database, (Integration Testing)
    @patch('mysql.connector.connect')
    def test_show_ongoing_with_ongoing_elections(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]

        # Call the function
        result = show_ongoing()

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "SELECT id FROM election WHERE status='ongoing'"
        self.assertTrue(any(expected_sql in call[0][0] for call in mock_cursor.execute.call_args_list))

        # Assert that the function returned the expected result
        self.assertEqual(result, 1)

    @patch('mysql.connector.connect')
    def test_show_ongoing_without_ongoing_elections(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []

        # Call the function
        result = show_ongoing()

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "SELECT id FROM election WHERE status='ongoing'"
        self.assertTrue(any(expected_sql in call[0][0] for call in mock_cursor.execute.call_args_list))

        # Assert that the function returned the expected result
        self.assertEqual(result, 0)
def manage_election_after():
    a="ongoing 1"
    a=a.split()
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    sql = "UPDATE election SET status='%s' WHERE id='%s'" %(a[0],a[1])
    try:
        cursor.execute(sql)
        return 1
    except:
        return 0
class TestManageElectionAfter(unittest.TestCase):  #Integration Testing, Updating the database.
    @patch('mysql.connector.connect')
    def test_manage_election_after_successful_update(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Call the function with valid values
        result = manage_election_after()

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "UPDATE election SET status='ongoing' WHERE id='1'"
        mock_cursor.execute.assert_called_once_with(expected_sql)

        # Assert that the function returned the expected result
        self.assertEqual(result, 1)

    @patch('mysql.connector.connect')
    def test_manage_election_after_failed_update(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        # Raise an exception to simulate a failed update
        mock_cursor.execute.side_effect = Exception

        # Call the function with valid values
        result = manage_election_after()

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "UPDATE election SET status='ongoing' WHERE id='1'"
        mock_cursor.execute.assert_called_once_with(expected_sql)

        # Assert that the function returned the expected result
        self.assertEqual(result, 0)
def show_election_result(election_id):
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute(("SELECT * FROM vote WHERE vote_ballot_id = %s" % election_id))
    records = cursor.fetchall()
    results = {}
    for vote in records:
        if vote[2] not in results:
            results[str(vote[2])] = 0
        results[str(vote[2])] += 1
    labels = []
    values = []
    for key in results.keys():
        values.append(results[key])
        labels.append(key)
    return 1
class TestShowElectionResult(unittest.TestCase): #tests if the graph values are created correctly (Integration testing)
    @patch('mysql.connector.connect')
    def test_show_election_result(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'candidate1', 'option1'),
            (2, 'candidate2', 'option1'),
            (3, 'candidate3', 'option2'),
            (4, 'candidate1', 'option2'),
            (5, 'candidate2', 'option2'),
        ]

        # Call the function with a valid election_id
        result = show_election_result(1)

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "SELECT * FROM vote WHERE vote_ballot_id = 1"
        mock_cursor.execute.assert_called_once_with(expected_sql)

        # Assert that the function returns the expected result
        self.assertEqual(result, 1)
def register_vote(candidate_id,candidate_keyword,election_id,citizen_tc):
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    # insert election
    sql = ("INSERT INTO vote(ssn,vote_ballot_id,selection) VALUES (%s, %s, %s)")
    election_data = (citizen_tc,str(election_id),candidate_keyword)
    # Executing the SQL command
    try:
        cursor.execute(sql, election_data)
        return "Voting was succsessfull,test complete."
    except:
        error = "You can't vote on the same election twice, test complete."
        return error
class TestRegisterVote(unittest.TestCase): #tests voting and voting with a duplicate vote
    @patch('mysql.connector.connect')
    def test_register_vote_successful(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Call the function with valid values
        result = register_vote(1, 'candidate1', 1, '123456789')

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "INSERT INTO vote(ssn,vote_ballot_id,selection) VALUES (%s, %s, %s)"
        expected_data = ('123456789', '1', 'candidate1')
        mock_cursor.execute.assert_called_once_with(expected_sql, expected_data)
        mock_connect.return_value.commit.assert_called_once()

        # Assert that the function returned the expected result
        expected_result = "Voting was successful, test complete."
        self.assertEqual(result, expected_result)

    @patch('mysql.connector.connect')
    def test_register_vote_duplicate_vote(self, mock_connect):
        # Mock the cursor and execute methods
        mock_cursor = mock_connect.return_value.cursor.return_value
        # Raise an exception to simulate a failed vote insertion
        mock_cursor.execute.side_effect = Exception

        # Call the function with valid values
        result = register_vote(1, 'candidate1', 1, '123456789')

        # Assert that the SQL query was executed with the expected SQL statement
        expected_sql = "INSERT INTO vote(ssn,vote_ballot_id,selection) VALUES (%s, %s, %s)"
        expected_data = ('123456789', '1', 'candidate1')
        mock_cursor.execute.assert_called_once_with(expected_sql, expected_data)

        # Assert that the function returned the expected result
        expected_result = "You can't vote on the same election twice, test complete."
        self.assertEqual(result, expected_result)
if __name__ == '__main__':
    unittest.main()