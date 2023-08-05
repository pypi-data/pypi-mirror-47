class ControlTextArea extends ControlBase {

    init_control() {
        var html = `<div id='${this.place_id()}' class='field control ControlTextArea' >
		    <label>${this.properties.label}</label>
		    <textarea placeholder='${this.properties.label}' type='text' 
		    rows='${this.properties.rows}' cols='${this.properties.cols}'
		    name='${this.name}' id='${this.control_id()}' ></textarea>
		</div>`;
        this.jquery_place().replaceWith(html);

        this.set_value(this.properties.value);

        var self = this;
        this.jquery().change(function () {
            self.basewidget.fire_event(this.name, 'update_control_event');
        });

        if (this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
    };

    ////////////////////////////////////////////////////////////////////////////////

}

	