import React, { useState } from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

function ToggleOnceCheckbox({ isChecked, onChange }) {
  // Event handler to handle checkbox click
  const handleCheckboxClick = (e) => {
		onChange(e.target.checked);
  };

	// idk GPT 
  return (
    <FormControlLabel
			sx = {{
				display: "flex",
				marginRight: 0,
				maringLeft: 50,
			}}
      control={
        <Checkbox
          checked={isChecked}
          color="success"
          disabled={isChecked} // Disable the checkbox when isChecked is true
          onChange={(e)=> handleCheckboxClick(e)}
        />
      }
			label=""
    />
  );
}

export default ToggleOnceCheckbox;
