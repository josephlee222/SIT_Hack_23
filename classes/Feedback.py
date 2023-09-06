class Feedback:
    def __init__(self,useremail,counselloremail, q1,q2,experience_details,comments):
        self.useremail = useremail
        self.counselloremail = counselloremail
        self.q1 = q1
        self.q2 = q2
        self.experience_details = experience_details
        self.comments = comments
        
    def set_useremail(self,useremail):
        self.useremail=useremail
    def get_useremail(self):
        return self.useremail
    
    def set_counselloremail(self,counselloremail):
        self.counselloremail=counselloremail
    def get_counselloremail(self):
        return self.counselloremail
    
    def set_q1(self,q1):
        self.q1=q1
    def get_q1(self):
        return self.q1
    
    def set_q2(self,q2):
        self.q2=q2
    def get_q2(self):
        return self.q2
    
    def set_experience_details(self,experience_details):
        self.experience_details=experience_details
    def get_experience_details(self):
        return self.experience_details
    
    def set_comments(self,comments):
        self.comments=comments
    def get_comments(self):
        return self.comments
    