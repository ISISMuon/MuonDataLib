var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.Button = function (props) {
    const {setData, data} = props;

    function onClick() {
        setData();
    }
    let Icon;
    Icon = React.createElement('i', {className: props.Icon,});
    return React.createElement(
        'Button',
        {
	    onClick,
            style: {
                margin: props.margin,
		'background-color': props.color,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
            },
        },
	Icon,
        props.value
    );
};
