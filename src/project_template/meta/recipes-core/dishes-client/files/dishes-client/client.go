package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

type Client struct {
	UpgradeID uint64 `json:"upgrade_id,string"`
	Filename  string `json:"file_name"`
	Verison   string `json:"version"` // 版本
	Update    int    `json:"update"`  // 0-不更新；1-更新
	Event     string `json:"event"`   // 事件
	Stage     string `json:"stage"`   // 固件阶段 dev or test or release
	Size      string `json:"size"`    // 大小
}

const (
	updateCommandSuffix = "/api/v1/client/update-command"
	updateEventSuffix   = "/api/v1/client/update-event"
	fileDownloadSuffix  = "/api/v1/firmwares/downloads"
)

func HttpClient(baseUrl string, interval int, product_id, device_id, path string) error {
	var client Client

	for {
		log.Println(baseUrl + updateCommandSuffix + "/" + device_id)
		err := httpGet(baseUrl+updateCommandSuffix+"/"+device_id, &client)
		if err != nil {
			return err
		}

		// 如果接收到更新命令，拉取固件并开始更新
		if client.Update == 1 {
			fileUrl := baseUrl + fileDownloadSuffix + "/" + product_id + "/" + client.Stage + "/" + client.Verison + "/" + client.Filename
			log.Println(fileUrl)
			err = fileDownloader(fileUrl, &client, path)
			if err != nil {
				return err
			}

			log.Println(client)

			postUrl := baseUrl + updateEventSuffix + "/" + strconv.FormatUint(client.UpgradeID, 10)
			log.Println(postUrl)
			err = httpPost(postUrl, &Client{
				Event: "start_update",
			})
			if err != nil {
				return err
			}

			err = Install(path + "/" + client.Filename)
			if err != nil {
				httpPost(postUrl, &Client{
					Event: "error_update",
				})
				return err
			} else {
				httpPost(postUrl, &Client{
					Event: "success_update",
				})
				return nil
			}
		}

		time.Sleep(time.Second * time.Duration(interval))
	}
}

func httpGet(baseUrl string, c *Client) error {
	resp, err := http.Get(baseUrl)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	content, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	err = json.Unmarshal(content, c)
	if err != nil {
		return err
	}

	return nil
}

func httpPost(baseUrl string, c *Client) error {
	data, err := json.Marshal(c)
	if err != nil {
		return err
	}

	resp, err := http.Post(baseUrl, "application/json", bytes.NewBuffer([]byte(data)))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return errors.New("return code error")
	}

	return nil
}

func fileDownloader(fileUrl string, c *Client, path string) error {

	file, err := os.Create(path + "/" + c.Filename)
	if err != nil {
		return err
	}

	defer file.Close()
	resp, err := http.Get(fileUrl)
	if err != nil {
		return err
	}

	defer resp.Body.Close()

	n, err := io.Copy(file, resp.Body)
	if err != nil {
		return err
	}

	size, err := strconv.ParseInt(c.Size, 10, 64)
	if err != nil {
		return err
	}

	if n != size {
		os.Remove(c.Filename)
		return errors.New("file length incorrect")
	}

	return nil
}
