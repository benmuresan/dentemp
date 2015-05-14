var app = angular.module('myApp', ['multipleDatePicker']);

//This controller is on the User side.
app.controller('demoController', ['$scope', '$http', function ($scope, $http) {
    //Gets dates that have already been selected and displays them on the calendar.
    $scope.selectedDays = [moment().date().valueOf()];
    $http.get('/dates_clicked/')
        .then(function (res) {
            console.log(res)
            ////# -------------------------------------------------------------
            //var correctData_list = [];
            //for(
            //    date in Json.parse(res.data);
            //    var correctData = date + "UTC")
            //    correctData_list.append(correctData);
            //)
            //$scope.selectedDays = correctData_list;
            ////# -----------------------------------------------------------
            $scope.selectedDays = JSON.parse(res.data);
        });


    //console.log(moment().date(5).valueOf())
    $scope.dayClick = function (time, selected) {
        console.log(selected.valueOf());
        console.log(selected.selected);
        console.log($scope.selectedDays)

        var formData = new FormData();
        formData.append("date_available", selected.valueOf());
        console.log(formData)

        var request = new XMLHttpRequest();
        console.log(formData)
        if (!selected.selected) {
            console.log("is selected")
            request.open("POST", "/add_date/");

        }
        else {
            console.log("is not selected")
            request.open("POST", "/remove_date/");
        }
        request.send(formData);
    };
}]);


//This controller returns the employees available for the selected day, or creates a event.
app.controller('officeController', ['$scope', function ($scope) {
    $scope.dayClick = function (time, selected) {
        //console.log(selected.valueOf());
        //console.log(selected.selected);
        //console.log($scope.selectedDays)

        if (document.getElementById("user_assistant").checked) {
            type_user = "assistant";
        } else {
            type_user = "hygienist";
        }

        var formData = new FormData();
        formData.append("type_user", type_user);
        formData.append("date_needed", selected.valueOf());
        console.log(formData)

        var request = new XMLHttpRequest();
        console.log(formData)
        if (!selected.selected) {
            console.log("is selected")
            request.open("POST", "/add_office_event/");

        }
        else {
            console.log("is not selected")
            request.open("POST", "/remove_date/");
        }
        request.send(formData);
    };


    $scope.logMonthChanged = function (newMonth, oldMonth) {
        alert('new month : ' + newMonth.format('YYYY-M-DD') + ' || old month : ' + oldMonth.format('YYYY-M-DD'));
    };

    $scope.doDate = function (event, date) {
        if (event.type == 'click') {
            alert(moment(date).format('YYYY-M-DD') + ' has been ' + (date.selected ? 'un' : '') + 'selected');
        } else {
            console.log(moment(date) + ' has been ' + event.type + 'ed')
        }
    };

    $scope.oneDayOff = [moment().date(14).valueOf()];
    //Todo
    $scope.selectedDays = [moment().date(4).valueOf(), moment().date(5).valueOf(), moment().date(8).valueOf()];
}]);