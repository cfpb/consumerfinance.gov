import React from "react";

import { ReactComponent as PlusSign } from "../../../img/plus-sign-icon.svg";
import { ReactComponent as ErrorIcon } from "../../../img/error-icon-round.svg";
import { ReactComponent as DollarSignIcon } from "../../../img/dollar-sign.svg";
import { ReactComponent as PencilEditIcon } from "../../../img/pencil-edit.svg";
import { ReactComponent as StarIcon } from "../../../img/star-icon.svg";
import { ReactComponent as ExclamationPointIcon } from "../../../img/exclamation-point.svg";
import { ReactComponent as LightBulb } from "../../../img/light-bulb.svg";
import { ReactComponent as FacebookIcon } from "../../../img/facebook-square.svg";
import { ReactComponent as TwitterIcon } from "../../../img/twitter-square.svg";
import { ReactComponent as LinkedInIcon } from "../../../img/linkedin-square.svg";
import { ReactComponent as FlickrIcon } from "../../../img/flickr-square.svg";
import { ReactComponent as YouTubeIcon } from "../../../img/youtube-square.svg";
import { ReactComponent as ExternalLinkIcon } from "../../../img/external-link.svg";
import { ReactComponent as UpArrowIcon } from "../../../img/up-arrow.svg";
import { ReactComponent as SaveIcon } from "../../../img/disk.svg";

// import "../../styles/Icon.scss";

export const Icon = ({ type }) => {
  return (
    <div className="icon-background">
      {(() => {
        switch (type) {
          case "close-icon":
            return <ErrorIcon className="plus-minus-icon" />;
          case "pencil-edit-icon":
            return <PencilEditIcon className="pencil-edit-icon" />;
          case "dollar-sign-icon":
            return <DollarSignIcon className="dollar-sign-icon" />;
          case "open-icon":
            return <PlusSign className="plus-minus-icon" />;
          case "star-icon":
            return <StarIcon className="star-icon" />;
          case "exclamation-point":
            return <ExclamationPointIcon className="exclamation-point" />;
          case "light-bulb":
            return <LightBulb className="light-bulb" />;
          case "facebook-icon":
            return <FacebookIcon className="social-media-icon" />;
          case "twitter-icon":
            return <TwitterIcon className="social-media-icon" />;
          case "linkedin-icon":
            return <LinkedInIcon className="social-media-icon" />;
          case "youtube-icon":
            return <YouTubeIcon className="social-media-icon" />;
          case "flickr-icon":
            return <FlickrIcon className="social-media-icon" />;
          case "up-arrow-icon":
            return <UpArrowIcon className="up-arrow-icon" />;
          case "external-link-icon":
            return <ExternalLinkIcon className="external-link-icon" />;
          case "save-icon":
            return <SaveIcon className="save-icon" />;
          default:
            return <div>There is an error on the Icon component</div>;
        }
      })()}
    </div>
  );
};
