
import axios from 'axios';
import { envs } from '../../config/envs';
import { GeocodeEntity } from '../../domain/entities/geocode.entity';


const https = require('https');

const agent = new https.Agent({ 
  rejectUnauthorized: false
});

export class GeocodeService {


  async geocodeFromApi(city: string): Promise<GeocodeEntity | any> {
    try {
      const response = await axios.get(`${envs.WEATHER_API_GEO_URL}`, {
        params: {
          q: city,
          limit: 1,
          appid: envs.WEATHER_API_KEY
        },
        httpsAgent: agent
      });
      const { lat, lon } = response.data[0];
      return GeocodeEntity.fromObject({ city: city, latitude: lat, longitude: lon });
    } catch (error) {
      return error;
    }
  };

  
}

