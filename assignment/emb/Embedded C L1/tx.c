#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to calculate CRC-16/XMODEM checksum
unsigned short calculate_checksum(unsigned char *data, int length) {
    unsigned short crc = 0;
    int i, j;
    for (i = 0; i < length; ++i) {
        crc ^= (unsigned short)data[i] << 8;
        for (j = 0; j < 8; ++j) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x1021;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc;
}

// Function to generate a packet
void generate_packet(unsigned short packet_number, unsigned short total_image_size, unsigned char *payload, int payload_size) {
    // Calculate packet length
    int packet_length = 7 + payload_size;  // 7 bytes for header, length, number, size, footer

    // Allocate memory for packet
    unsigned char *packet = (unsigned char *)malloc(packet_length);

    // Fill packet structure
    packet[0] = 0x7D;  // Header
    packet[1] = (unsigned char)packet_length;  // Packet length
    packet[2] = (unsigned char)(packet_number >> 8);  // MSB of packet number
    packet[3] = (unsigned char)packet_number;  // LSB of packet number
    packet[4] = (unsigned char)(total_image_size >> 8);  // MSB of total image size
    packet[5] = (unsigned char)total_image_size;  // LSB of total image size
    memcpy(packet + 6, payload, payload_size);  // Copy payload
    unsigned short crc = calculate_checksum(packet + 1, packet_length - 3);  // Calculate CRC
    packet[packet_length - 2] = (unsigned char)(crc >> 8);  // MSB of CRC
    packet[packet_length - 1] = (unsigned char)crc;  // LSB of CRC

    // Print packet
    printf("Generated Packet %d: ", packet_number);
    for (int i = 0; i < packet_length; ++i) {
        printf("%02X ", packet[i]);
    }
    printf("\n");

    // Free allocated memory
    free(packet);
}

// Example usage
int main() {
    // Example image data
    unsigned char image_data[] = "This is a sample image.";

    // Split image data into packets
    int image_size = strlen((const char *)image_data);
    int packet_size = 10;  // Example packet size
    int num_packets = (image_size + packet_size - 1) / packet_size;
    int i;
    for (i = 0; i < num_packets; ++i) {
        unsigned short packet_number = i + 1;
        int remaining_bytes = image_size - i * packet_size;
        int payload_size = remaining_bytes < packet_size ? remaining_bytes : packet_size;
        generate_packet(packet_number, image_size, image_data + i * packet_size, payload_size);
    }

    return 0;
}
