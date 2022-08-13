// add an event listener to #id_province which is an 'select input'
// when the user selects a province, the event listener will
// window.addEventListener("load", function(){
//     var province = document.getElementById('id_province');
//     var city = document.getElementById('id_city');
//     city.innerHTML = `<select name="city" required="" id="id_city">
//     <option value="" selected="">---------</option>
// </select>`
//     province.addEventListener('change', function(){
//         // ajax
//         // get the list of cities from the server by giving it the province id
//         // when the server responds, the event listener will add the cities to the city select input
//         var xhr = new XMLHttpRequest();
//         console.log(this.value);
//         xhr.open('GET', '/CustomUser/ajax/get_cities_of_province/?province_id=' + this.value, true);
//         xhr.onreadystatechange = function() {
//             if (xhr.readyState == 4 && xhr.status == 200) {
//                 city.innerHTML = xhr.responseText;
//             }
//         }
//         xhr.send();
//     });
// });

