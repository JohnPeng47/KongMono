import axios from "axios";

export const ENDPOINT = "http://localhost:8000";
const AUTHENTICATE_ENDPOINT = ENDPOINT + "/authenticate";

type AuthenticateRequest = {
  username: string;
};

// interface RequestSuccess {
//   status: 'success';
// }

// interface RequestError {
//   status: 'error';
// }

// interface RequestLoading {
//   status: 'loading';
// }

// type RequestStatus = RequestSuccess | RequestError | RequestLoading;

// enum RequestStatus {
//   Success = 'success',
//   Error = 'error',
//   Loading = 'loading'
// }

export class BaseHTTPRequest {
  private static instance: BaseHTTPRequest;
  private static token: string | null = null;

  public static async initializeToken(): Promise<void> {
    const storedToken = localStorage.getItem("client_token");
    if (storedToken) {
      this.token = storedToken;
    } else {
      const requestBody: AuthenticateRequest = {
        username: "johnpeng", // Determine how you want to provide this username
      };

      try {
        const response = await axios.post(AUTHENTICATE_ENDPOINT, requestBody);
        this.token = response.data.token;
        localStorage.setItem("client_token", this.token);
      } catch (error) {
        console.error("Error authenticating user:", error);
      }
    }
  }

  public static get(endpoint: string, params?: any): () => Promise<any> {
    return this.request("GET", endpoint, params);
  }

  public static post(endpoint: string, data?: any): () => Promise<any> {
    return this.request("POST", endpoint, data);
  }

  // This currently returns an axios function.. very retarded, will change later
  private static request(
    method: "GET" | "POST",
    endpoint: string,
    dataOrParams?: any,
  ): () => Promise<any> {
    if (!BaseHTTPRequest.token) {
      throw new Error("Token not initialized");
    }

    const config = {
      method,
      url: endpoint,
      headers: {
        Authorization: `Bearer ${BaseHTTPRequest.token}`,
      },
    };

    if (method === "GET") {
      config["params"] = dataOrParams;
    } else {
      config["data"] = dataOrParams;
    }

    // this is pretty retarded right now
    return () => {
      return axios(config);
    };
  }
}
