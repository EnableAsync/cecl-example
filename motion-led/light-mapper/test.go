package main

import (
	"crypto/tls"
	"fmt"
	"sync"

	MQTT "github.com/eclipse/paho.mqtt.golang"
)

func OnCameraReceived(client MQTT.Client, message MQTT.Message) {
	fmt.Println(string(message.Payload()))
}

func main() {
	ClientOpts := HubClientInit("mqtt://192.168.43.197:1883", "eventbus", "", "")
	Client := MQTT.NewClient(ClientOpts)
	if Token_client := Client.Connect(); Token_client.Wait() && Token_client.Error() != nil {
		fmt.Println("client.Connect() Error is ", Token_client.Error())
	}

	// for {
	// 	token := Client.Publish("test", 0, false, "test")
	// 	time.Sleep(1 * time.Second)
	// 	token.Wait()
	// 	if token.Error() != nil {
	// 		fmt.Println(token.Error())
	// 	}
	// 	fmt.Println("published")
	// }

	var wg sync.WaitGroup
	wg.Add(1)

	cameraClient := Client.Subscribe("camera", 0, OnCameraReceived)
	if cameraClient.Wait() && cameraClient.Error() != nil {
		fmt.Println(cameraClient.Error())
	}

	wg.Wait()
}

// HubclientInit create mqtt client config
func HubClientInit(server, clientID, username, password string) *MQTT.ClientOptions {
	opts := MQTT.NewClientOptions().AddBroker(server).SetClientID(clientID).SetCleanSession(true)
	if username != "" {
		opts.SetUsername(username)
		if password != "" {
			opts.SetPassword(password)
		}
	}
	tlsConfig := &tls.Config{InsecureSkipVerify: true, ClientAuth: tls.NoClientCert}
	opts.SetTLSConfig(tlsConfig)
	return opts
}
