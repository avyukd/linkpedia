
		
		function myFunction(data){

			var map = new google.maps.Map(document.getElementById("map"), {zoom: 1, center: {lat:0,lng:0}});
            for (i = 0; i < data.length; i++) {
                var marker = new google.maps.Marker({
                    position: data[i],
                    map: map
                });
            }
			for (k = 0; k < data.length; k+=2){
				var path = new google.maps.Polyline({
					path: [data[k],data[k+1]],
					geodesic: true,
					strokeColor: '#FF0000',
					strokeOpacity: 1.0,
					strokeWeight: 2
				})
				path.setMap(map);
			}
		}
		
            /*var flightPath = new google.maps.Polyline({
                path: [{lat:0,lng:0},{lat:100,lng:100}],
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });*/
            //flightPath.setMap(map);

        