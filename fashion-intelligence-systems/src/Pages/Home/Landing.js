import React, { Component } from "react";
// import * as action from "../redux/registerRedux/registerAction";
import { connect } from "react-redux";
import Notifications from "react-notification-system-redux";
import Header from "./Header";
import Footer from "./footer.js";
import {
  Redirect,
  BrowserRouter as Router,
  Route,
  Switch,
} from "react-router-dom";

import Blogs from "../Blogs.jsx";
import Model from "../Model.jsx";
import Dashboard from "./dashboard.js";
import { HTML5Backend } from "react-dnd-html5-backend";
import Category  from "./category";
class Landing extends Component {
  componentWillReceiveProps(){
    if(!this.props.loading){

  const el = document.querySelector(".loader-container");
      if (el) {
        el.remove();  // removing the spinner element        this.setState({ loading: false }); // showing the app      }
    }
    }
  }

  render() {
    return (
      <>
        {this.props.loggedIn && (
          <Notifications notifications={this.props.notifications} />
        )}
        <Header />
        <Switch>
          <Route path="/home/blogs" component={() => <Blogs />} />
          <Route
            path="/home/model"
            component={() => <Model backend={HTML5Backend} />}
          />
          <Route path="/home/category/:category" render={props => <Category {...props} />} />
          <Route path="/home/dashboard" component={() => <Dashboard />} />
          <Redirect from="/home" to="/home/dashboard" />
        </Switch>
        <Footer/>
      </>
    );
  }
}

const mapStateToProps = state => {
  console.log(state);
  return {
    loggedIn: state.loginReducer.loggedIn,
    //   error: state.loginReducer.error,
    notifications: state.notifications,
    loading: state.dataReducer.loading,
  };
};

// const mapDispatchToProps = dispatch => {
//   return {
//     login: data => dispatch(action.login(data)),
//   };
// };

export default connect(mapStateToProps)(Landing);
