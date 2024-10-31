// auth-front/src/auth/requestNewAccessToken.ts
import { AccessTokenResponse } from "../types/types";
import { API_URL } from "./authConstants";

export default async function requestNewAccessToken(refreshToken: string): Promise<string | null> {
  try {
    const response = await fetch(`${API_URL}/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${refreshToken}`,
      },
    });

    if (response.ok) {
      const json = (await response.json()) as AccessTokenResponse;
      if (json.error) {
        throw new Error(json.error);
      }
      return json.access_token;
    } else {
      throw new Error("Unable to refresh access token.");
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}
