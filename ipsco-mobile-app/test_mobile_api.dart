import 'dart:convert';
import 'package:http/http.dart' as http;

class MobileApiTest {
  static const String baseUrl = 'https://ipsco.onrender.com';
  static const String apiBase = '$baseUrl/api';

  // Test de connexion à l'API
  static Future<bool> testApiConnection() async {
    try {
      final response = await http.get(Uri.parse(baseUrl));
      print('✅ Site principal accessible: ${response.statusCode}');
      return response.statusCode == 200;
    } catch (e) {
      print('❌ Erreur de connexion: $e');
      return false;
    }
  }

  // Test de l'endpoint de connexion
  static Future<bool> testLoginEndpoint() async {
    try {
      final response = await http.post(
        Uri.parse('$apiBase/login/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': 'test',
          'password': 'test'
        }),
      );
      print('✅ Endpoint login accessible: ${response.statusCode}');
      return response.statusCode == 401; // 401 est normal (pas de credentials valides)
    } catch (e) {
      print('❌ Erreur endpoint login: $e');
      return false;
    }
  }

  // Test de l'endpoint des missions chauffeur
  static Future<bool> testChauffeurMissions() async {
    try {
      final response = await http.get(Uri.parse('$apiBase/chauffeur/missions/'));
      print('✅ Endpoint missions chauffeur accessible: ${response.statusCode}');
      return response.statusCode == 401; // 401 est normal (pas de token)
    } catch (e) {
      print('❌ Erreur endpoint missions: $e');
      return false;
    }
  }

  // Test complet de l'API
  static Future<void> runAllTests() async {
    print('🧪 Test de l\'API IPS-CO pour l\'application mobile');
    print('=' * 50);

    final connectionOk = await testApiConnection();
    final loginOk = await testLoginEndpoint();
    final missionsOk = await testChauffeurMissions();

    print('\n' + '=' * 50);
    print('📊 Résumé des tests:');
    print('✅ Connexion au site: ${connectionOk ? "OK" : "ÉCHEC"}');
    print('✅ Endpoint login: ${loginOk ? "OK" : "ÉCHEC"}');
    print('✅ Endpoint missions: ${missionsOk ? "OK" : "ÉCHEC"}');

    if (connectionOk && loginOk && missionsOk) {
      print('\n🎉 Tous les tests sont réussis !');
      print('📱 Votre application mobile peut se connecter à l\'API.');
    } else {
      print('\n⚠️ Certains tests ont échoué.');
      print('🔧 Vérifiez la configuration de l\'API.');
    }
  }
}

void main() async {
  await MobileApiTest.runAllTests();
}
