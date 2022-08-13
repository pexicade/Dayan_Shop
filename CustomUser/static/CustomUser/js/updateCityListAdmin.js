$(document).ready(function(){

    $("#id_province").change(load_cities);
    var href = window.location.href;
    href = href.slice(0,href.length-1);
    var state = href.slice(href.lastIndexOf('/')+1);
    if (state === 'add'){
        console.log('add');
    }else if (state === 'change'){
        var id = href.slice(0,href.lastIndexOf('/'));
        id = id.slice(id.lastIndexOf('/')+1);
        console.log(`change ${id}`);
        const url = "http://127.0.0.1:8000/user/ajax/load_province_and_city/";
        $.ajax({
            url: url,
            data: {
                address_id: id
            },
            success: function(data){
                console.log(data);
                if (data.status==="OK"){
                    console.log(document.getElementById("id_province"), parseInt(data.province_id));
                    document.getElementById("id_province").selectedIndex = parseInt(data.province_id)-1;
                    console.log(document.getElementById("id_city").selectedIndex);
                    // load_cities();
                    console.log(document.getElementById("id_city").selectedIndex, parseInt(data.city_id));
                    document.getElementById("id_city").value = parseInt(data.city_id);
                    // document.getElementById('id_city').value = parseInt(data.city_id);
                }
            }
        });
    }

    function load_cities(){
        console.log("ajax");
        const url = "http://127.0.0.1:8000/user/ajax/load_cities";
        const province_id = $("#id_province").val();
        $.ajax({
            url: url,
            data: {
                province_id: province_id
            },
            success: function(data){
                $("select[name='city']").html(data)
            }
        });
    } 
});