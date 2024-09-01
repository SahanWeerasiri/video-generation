import 'package:flutter/material.dart';

class SummaryGalleryScreen extends StatelessWidget {
  final List<Map<String, dynamic>> data;

  const SummaryGalleryScreen({Key? key, required this.data}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Summary Gallery'),
      ),
      body: ListView.builder(
        itemCount: data.length,
        itemBuilder: (context, index) {
          final milestone = data[index];
          return Card(
            margin: EdgeInsets.all(10),
            child: ExpansionTile(
              title: Text('${milestone['time']} - ${milestone['location']['name']}'),
              children: milestone['content'].map<Widget>((mediaPath) {
                return ListTile(
                  leading: Icon(Icons.image),
                  title: Text(mediaPath),
                );
              }).toList(),
            ),
          );
        },
      ),
    );
  }
}
