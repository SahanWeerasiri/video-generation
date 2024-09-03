import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'video_player_screen.dart';

class SummaryGalleryScreen extends StatelessWidget {
  final List<Map<String, dynamic>> data;

  SummaryGalleryScreen({Key? key, required this.data}) : super(key: key);

  var msg = 'Start Generation';

  Future<void> startGeneration(BuildContext context) async {
    /*try {
      // Extract all fields other than 'content' from each entry in data
      final List<Map<String, dynamic>> dataWithoutContent = data.map((entry) {
        // Remove 'content' key and keep all other key-value pairs
        return Map<String, dynamic>.fromEntries(
          entry.entries.where((e) => e.key != 'content'),
        );
      }).toList();

      // Encode pathsOnly as JSON and send it to the server
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/generate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'data': dataWithoutContent}),
      );

      // Decode response
      final decoded = json.decode(response.body) as Map<String, dynamic>;

      // Get the generated video path from the response
      final videoPath = decoded['video_path'] as String;

      // Navigate to the VideoPlayerScreen and pass the video path
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => VideoPlayerScreen(
              videoPath: videoPath), // Pass the video path correctly
        ),
      );
    } catch (error) {
      print('Error during generation: $error');
      msg = 'Error during generation';
    }*/
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => VideoPlayerScreen(
            videoPath:
                "C:\\Users\\SAHAN\\Desktop\\test_\\combined_video.mp4"), // Pass the video path correctly
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: ElevatedButton(
          onPressed: () => startGeneration(context),
          child: Text(msg),
        ),
      ),
      body: ListView.builder(
        itemCount: data.length,
        itemBuilder: (context, index) {
          final milestone = data[index];
          return Card(
            margin: EdgeInsets.all(10),
            child: ExpansionTile(
              title: Text(
                  '${milestone['time']} - ${milestone['location']['name']}'),
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: SizedBox(
                    height: 200,
                    child: GridView.builder(
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 3,
                        crossAxisSpacing: 4.0,
                        mainAxisSpacing: 4.0,
                      ),
                      itemCount: milestone['content'].length,
                      itemBuilder: (context, mediaIndex) {
                        return Stack(
                          fit: StackFit.expand,
                          children: [
                            Image.memory(
                              milestone['content'][mediaIndex],
                              fit: BoxFit.cover,
                              errorBuilder: (context, error, stackTrace) {
                                print('Error loading image: $error');
                                return Container(
                                  color: Colors.grey[300],
                                  child: Icon(Icons.error, color: Colors.red),
                                );
                              },
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
