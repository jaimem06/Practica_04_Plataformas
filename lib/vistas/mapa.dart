import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:practica_04_movil/controller/Coneccion.dart';
import 'package:practica_04_movil/models/ResponseGeneric.dart';

class UbicacionSucursales extends StatefulWidget {
  const UbicacionSucursales({super.key});

  @override
  UbicacionSucursalesState createState() => UbicacionSucursalesState();
}

class UbicacionSucursalesState extends State<UbicacionSucursales> {
  final Connection connection = Connection();
  List<Marker> markers = [];
  bool isLoading = true;
  late MapController mapController;

  @override
  void initState() {
    super.initState();
    mapController = MapController();
    fetchSensorLocations();
  }

  void fetchSensorLocations() async {
    try {
      ResponseGeneric response = await connection.getSucursalLocations();
      if (response.code == '200') {
        setState(() {
          markers = (response.datos as List).map((sensor) {
            return Marker(
              point: LatLng(sensor['latitud'], sensor['longitud']),
              width: 80.0,
              height: 80.0,
              //onTap: () => showSensorInfo(sensor),
              child: const Icon(
                Icons.location_on,
                color: Colors.blueAccent,
                size: 40,
              ),
            );
          }).toList();
          isLoading = false;
        });

        if (markers.isNotEmpty) {
          mapController.move(markers[0].point, 16.0);
        }
      } else {
        setState(() {
          isLoading = false;
        });
        print('Error: ${response.msg}');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      print('Error fetching sensor locations: $e');
    }
  }

  void showSensorInfo(Map<String, dynamic> sensor) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Información del sensor'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Text('ID: ${sensor['id']}'),
              Text('Latitud: ${sensor['latitud']}'),
              Text('Longitud: ${sensor['longitud']}'),
              Text('Tipo: ${sensor['tipo']}'),
              // Agrega más campos según la información disponible en 'sensor'
            ],
          ),
          actions: <Widget>[
            TextButton(
              child: Text('Cerrar'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    double width = MediaQuery.of(context).size.width * 0.90;
    double height = MediaQuery.of(context).size.height * 0.80;

    return Scaffold(
      body: Center(
        child: isLoading
            ? const CircularProgressIndicator() // Mostrar indicador de carga mientras se obtienen los datos
            : Container(
                margin: const EdgeInsets.all(20),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.blue.shade900, width: 2),
                  borderRadius: BorderRadius.circular(15),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 10,
                      offset: const Offset(0, 5),
                    ),
                  ],
                ),
                width: width,
                height: height,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(15),
                  child: FlutterMap(
                    mapController: mapController,
                    /*                     options: MapOptions(
                        center: markers.isNotEmpty
                            ? markers[0].point
                            : LatLng(0, 0),
                        zoom: 16,
                      ), */
                    children: [
                      TileLayer(
                        urlTemplate:
                            'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                        userAgentPackageName: 'com.example.app',
                      ),
                      RichAttributionWidget(
                        attributions: [
                          TextSourceAttribution(
                            'OpenStreetMap contributors',
                            onTap: () => Uri.parse(
                                'https://openstreetmap.org/copyright'),
                          ),
                        ],
                      ),
                      MarkerLayer(
                        markers: markers,
                      ),
                    ],
                  ),
                ),
              ),
      ),
    );
  }
}
