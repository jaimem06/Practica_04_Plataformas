import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:practica_04_movil/models/ResponseGeneric.dart';

class Connection {
  final String urlBase = "http://192.168.1.13:5000/";

  Future<ResponseGeneric> get(String resource,
      {String responseKey = 'datos'}) async {
    final String url = urlBase + resource;
    Map<String, String> headers = {'Content-Type': "application/json"};
    final uri = Uri.parse(url);
    final response = await http.get(uri, headers: headers);

    if (response.statusCode == 200) {
      Map<String, dynamic> body = jsonDecode(response.body);
      return _response(body['code'].toString(), body['msg'], body[responseKey]);
    } else {
      throw Exception('Error al cargar los datos');
    }
  }

  Future<ResponseGeneric> post(
      String resource, Map<String, dynamic> data) async {
    final String url = urlBase + resource;
    Map<String, String> headers = {'Content-Type': "application/json"};
    final uri = Uri.parse(url);
    final response =
        await http.post(uri, headers: headers, body: jsonEncode(data));

    if (response.statusCode == 200) {
      final body = jsonDecode(response.body);
      if (body == null ||
          !body.containsKey('code') ||
          !body.containsKey('msg') ||
          !body.containsKey('datos')) {
        throw Exception('Respuesta inesperada del servidor');
      }
      Map<String, dynamic> datos =
          body['datos'] != null ? Map<String, dynamic>.from(body['datos']) : {};
      return _response(body['code'].toString(), body['msg'], datos);
    } else {
      throw Exception('Failed to post data');
    }
  }

  ResponseGeneric _response(String code, String msg, dynamic datos) {
    var response = ResponseGeneric();
    response.msg = msg;
    response.code = code;
    response.datos = datos;
    return response;
  }

  Future<ResponseGeneric> getSucursalLocations() async {
    return get("sucursal");
  }

  Future<ResponseGeneric> getProductos() async {
    return get("producto");
  }

  Future<ResponseGeneric> login(Map<String, dynamic> credentials) async {
    return post("login", credentials);
  }

  Future<ResponseGeneric> getUsuario() async {
    return get("usuario");
  }
}
