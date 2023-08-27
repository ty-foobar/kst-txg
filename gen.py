import prof, student, trips
from sub import cls, replace

def main():
    #### 編集してください ######################
    currentTrip = trips.ccp2023()
    ##########################################

    prof_ = cls.Prof(prof.prof())
    student_ = cls.Student(student.student())
    trip = cls.Trip(*currentTrip)
    replace.main(prof_, student_, trip)

if __name__ == '__main__':
    main()
