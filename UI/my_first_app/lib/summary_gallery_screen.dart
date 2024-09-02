import 'package:flutter/material.dart';
import 'dart:typed_data';

class SummaryGalleryScreen extends StatelessWidget {
  final List<Map<String, dynamic>> data;

  const SummaryGalleryScreen({Key? key, required this.data}) : super(key: key);

  void startGeneration() {}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: ElevatedButton(
          onPressed: startGeneration,
          child: Text('Start Generation'),
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
                    height: 200, // Set a fixed height for the GridView
                    child: GridView.builder(
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount:
                            3, // Adjust the number of images in each row
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
