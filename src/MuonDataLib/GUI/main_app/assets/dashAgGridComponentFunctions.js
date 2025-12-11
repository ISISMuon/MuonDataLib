var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.Button = function (props) {
    const {setData, data} = props;

    function onClick() {
        setData();
    }
    let icon
    icon = React.createElement('i', {className: props.icon});
    return React.createElement(
        'Button',
        {
	    onClick,
            className: props.className   
	},
	icon,
    );
};
