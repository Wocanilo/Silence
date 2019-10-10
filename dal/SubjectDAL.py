# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.

from dal.BaseDAL import BaseDAL

class SubjectDAL(BaseDAL):

    def get_all(self):
        '''
        Get subject by OID
        -Input:
            *The OID of the subject that we want to get
        -Output:
            *Only one subject
            *None value if we cannot find the OID
        '''

        q = "SELECT * FROM Subjects"
        subjects = self.query(q)
        return subjects

    def get_by_oid(self, oid):
        '''
        Get subject by OID
        -Input:
            *The OID of the subject that we want to get
        -Output:
            *Only one subject
            *None value if we cannot find the OID
        '''

        subject = None
        q = "SELECT * FROM Subjects WHERE subjectId = %s"
        params = (oid,)

        res = self.query(q, params)
        if len(res) > 0:
            subject = res[0]

        return subject

    def get_by_acronym(self, acronym):
        '''
        Get subject by acronym
        -Input:
            *The acronym of the subject that we want to get
        -Output:
            *Only one subject
            *None value if we cannot find the acronym
        '''

        subject = None
        q = "SELECT * FROM Subjects WHERE acronym = %s"
        params = (acronym,)

        res = self.query(q, params)
        if len(res) > 0:
            subject = res[0]

        return subject

    def get_by_name(self, name):
        '''
        Get subject by name
        -Input:
            *The name of the subject that we want to get
        -Output:
            *Only one subject
            *None value if we cannot find the name
        '''

        subject = None
        q = "SELECT * FROM Subjects WHERE name = %s"
        params = (name,)

        res = self.query(q, params)
        if len(res) > 0:
            subject = res[0]

        return subject

    def insert(self, name, acronym, n_credits, course, subject_type, degreeId):
        '''
        Insert a new subject
        -Input:
            *All of the properties of the subject
        - Output:
            *The OID assigned to the subject that we have inserted
        '''

        q = "INSERT INTO Subjects (name, acronym, credits, course, type, degreeId) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (name, acronym, n_credits, course, subject_type, degreeId)
        res = self.execute(q, params)
        return res

    def update(self, oid, name, acronym, n_credits, course, subject_type, degreeId):
        '''
        Update one subject
        -Input:
            *All of the properties of the subject, including the OID that we want to update
        -Output:
            *The OID of the subject that we have updated
        '''

        q = "UPDATE Subjects SET name = %s, acronym = %s, credits = %s, course = %s, type = %s, degreeId = %s WHERE subjectId = %s"
        params = (name, acronym, n_credits, course, subject_type, degreeId, oid)
        res = self.execute(q, params)
        return res

    def delete(self, oid):
        '''
        Delete one subject
        -Input:
            *The OID of the subject that we want to delete
        -Output:
            *The OID of the subject that was deleted
        '''

        q = "DELETE FROM Subjects WHERE subjectId = %s"
        params = (oid,)
        res = self.execute(q, params)
        return res
