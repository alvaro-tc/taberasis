// auth-front/src/routes/Profile.tsx
import { useEffect, useState } from "react";
import PortalLayout from "../layout/PortalLayout";
import { useAuth } from "../auth/AuthProvider";
import { API_URL } from "../auth/authConstants";

interface UserProfile {
  username: string;
  roles: string[];
  email: string;
}

export default function Profile() {
  const auth = useAuth();
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);

  useEffect(() => {
    async function fetchUserProfile() {
      const accessToken = auth.getAccessToken();
      try {
        const response = await fetch(`${API_URL}/whoami`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (response.ok) {
          const json = await response.json();
          setUserProfile(json.user_details);
        } else {
          console.error("Failed to fetch user profile");
        }
      } catch (error) {
        console.error("An error occurred while fetching user profile", error);
      }
    }

    fetchUserProfile();
  }, [auth]);

  return (
    <PortalLayout>
      <div className="profile">
        <h1>Profile</h1>
        {userProfile ? (
          <div>
            <p><strong>Username:</strong> {userProfile.username}</p>
            <p><strong>Email:</strong> {userProfile.email}</p>
            
            <p><strong>Roles:</strong> {userProfile.roles?.join(", ")}</p>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </PortalLayout>
  );
}