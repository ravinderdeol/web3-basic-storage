// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract GradeStorage {
    // grade will default to zero upon contract deployment
    // grade has global scope so can be accessed throughout the contract
    uint256 grade;

    // student object is defined using a struct
    struct Student {
        string name;
        uint256 grade;
    }

    // array is created to store the student object
    Student[] public student;

    // take a key and return a variable with a mapping data structure
    mapping(string => uint256) public nameToGrade;

    // public function that changes the value of grade
    // function included for demonstration purposes
    function storeGrade(uint256 _grade) public {
        grade = _grade;
    }

    // view only function to return the grade and not change state
    // function included for demonstration purposes
    function readGrade() public view returns (uint256) {
        return grade;
    }

    // function stored in memory so it is wiped once execution stops
    // adds to the student array which changes state
    // maps the key name to the value grade
    function addStudent(string memory _name, uint256 _grade) public {
        student.push(Student({name: _name, grade: _grade}));
        nameToGrade[_name] = _grade;
    }
}
