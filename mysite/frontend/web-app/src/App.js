import React from "react";
import "./App.css";
import LoginPage from "./pages/LoginPage";
import Register from "./pages/Register";
import Homepage from "./pages/Homepage";
import Projects from "./pages/Projects";
import PeopleView from "./pages/PeopleView";
import SuggestionsForm from "./pages/Suggestions";
import Tasks from "./pages/Tasks";
import MeetingsForm from "./components/MeetingView";
import UserProfile from "./pages/UserProfile";
import { AuthProvider } from "./context/AuthContext";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route
              exact
              path="/"
              element={
                <PrivateRoute>
                  <Homepage />
                </PrivateRoute>
              }
            />
            <Route exact path="/login" element={<LoginPage />} />
            <Route exact path="/register" element={<Register />} />
            <Route path="/projects/:slug" element={<Projects />} />
            <Route path="/projects/:slug/people" element={<PeopleView />} />
            <Route path="/projects/:slug/tasks" element={<Tasks />} />
            <Route path="/projects/:slug/suggestions" element={<SuggestionsForm />} />
            <Route path="/projects/:slug/meetings" element={<MeetingsForm/>}/>
            <Route path= "/users/:slug"  element={<UserProfile/>}/>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
