var app = angular.module('myApp', ['multipleDatePicker']);

//This controller is on the User side.
app.controller('demoController', ['$scope', '$http', function ($scope, $http) {
console.log(print="works!");

    //Gets dates that have already been selected and displays them on the calendar.
    $scope.selectedDays = [moment().date().valueOf()];

    //Gets dates and adds the correct timeszone offset to the date. Then displays on calendar.
    $http.get('/dates_clicked/').then(function (responseObject) {
        //console.log(responseObject);
        var correctData = JSON.parse(responseObject.data);
        //console.log(correctData)

        var tempDate = new Date();
        var minutes_from_gmt = tempDate.getTimezoneOffset();
        var seconds_in_min = 60;
        var millis_in_seconds = 1000;
        var ts_delta = minutes_from_gmt * seconds_in_min * millis_in_seconds;

        for (var i = 0; i < correctData.length; i++) {
            var ts_source = correctData[i];


            //console.log(ts_source);
            var sourceDate = new Date(ts_source);
            //console.log(sourceDate);
            var ts_output = ts_source + ts_delta;
            var output_date = new Date(ts_output);
            //console.log(output_date)
            //var out = new Date(ts_output);
            correctData[i] = ts_output;
        }
        $scope.selectedDays = correctData;
    });

    //console.log(moment().date(5).valueOf())
    $scope.dayClick = function (time, selected) {
        //console.log(selected.valueOf());
        //console.log(selected.selected);
        //console.log($scope.selectedDays)

        var formData = new FormData();
        formData.append("date_available", selected.valueOf());
        //console.log(formData);

        var request = new XMLHttpRequest();
        console.log(formData)
        if (!selected.selected) {
            //console.log("is selected")
            request.open("POST", "/add_date/");

        }
        else {
            //console.log("is not selected")
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
        //console.log(formData);

        var request = new XMLHttpRequest();
        console.log(formData);
        if (!selected.selected) {
            //console.log("is selected")
            request.open("POST", "/add_office_event/");

        }
        else {
            //console.log("is not selected")
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