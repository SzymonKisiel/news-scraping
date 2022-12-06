import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Constants } from '../../model/constants';
import { API_URL } from '../../tokens';

@Injectable({
  providedIn: 'root'
})
export class CommandService {

  constructor(
    @Inject(API_URL) private apiUrl: string,
    private httpClient: HttpClient) { }

  apiPath = '/api/command-handler/'

  crawl() {
    const action = 'crawl'
    const url = this.apiUrl + this.apiPath + action
  }

  
  getAllDelays() {
    const action = 'get-delay'
    const url = this.apiUrl + this.apiPath + action
    const body = {
      "websites": Constants.WEBSITES
    }
    return this.httpClient.post(url, body)
  }
  
  getAllScrapingStarts() {
    const action = 'get-scraping-start'
    const url = this.apiUrl + this.apiPath + action
  }
  
  getWebsites() {
    const action = 'get-websites'
    const url = this.apiUrl + this.apiPath + action
    return this.httpClient.get(url) 
  }

  setDelay() {
    const action = 'set-delay'
    const url = this.apiUrl + this.apiPath + action
  }

  setScrapingStart() {
    const action = 'set-scraping-start'
    const url = this.apiUrl + this.apiPath + action
  }
}
