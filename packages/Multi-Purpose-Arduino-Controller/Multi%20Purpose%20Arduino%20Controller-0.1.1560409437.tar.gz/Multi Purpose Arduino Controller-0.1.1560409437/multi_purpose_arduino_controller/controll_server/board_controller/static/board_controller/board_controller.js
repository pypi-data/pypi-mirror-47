var all_ports = [];
var all_boards = {};
board_controller_portcontroller_div = null;
board_controller_div = $("#board_controller_div");
board_controller_container = $("<div><h5 name='title'></h5><form name='form'></form></div>");

function set_port_controller_div(portcontroller_div){
    board_controller_portcontroller_div =  portcontroller_div;
    for(let i=0;i<all_ports.length;i++){
        all_ports[i].set_port_controller_div(board_controller_portcontroller_div)
    }
}

function set_board_controller_div(new_board_controller_div){
    board_controller_div =  new_board_controller_div;
    for(let i=0;i<all_boards.length;i++){
        all_boards[i].set_board_controller_div(board_controller_div)
    }
}

class Port{
    constructor(port){
        this.port=port;
        this._create_html_representation();
        this.set_port_controller_div(board_controller_portcontroller_div);
    }

    _create_html_representation (){
        this._html_elements={};
        this._html_representation = $('<div></div>');
        this._html_elements.title = $("<lable>"+this.port+"</lable>");
        this._html_representation.append(this._html_elements.title);

        this._html_elements.activate_button=$("<button class='btn btn-warning'>activate</button>");
        this._html_representation.append(this._html_elements.activate_button);
        this._html_elements.activate_button.click(function () {
            wscs.send(wscs.commandmessage('activate_port', "gui", "server", true, [], {port:this.port}));
        }.bind(this));

        this._html_elements.deactivate_button=$("<button class='btn btn-danger'>deacivate</button>");
        this._html_representation.append(this._html_elements.deactivate_button);
        this._html_elements.deactivate_button.click(function () {
            wscs.send(wscs.commandmessage('deactivate_port', "gui", "server", true, [], {port:this.port}));
        }.bind(this));
        console.log(this);

        this._html_elements.custom_controll = $('<div class="portcontroller customcontroll"></div>');
        this._html_representation.append(this._html_elements.custom_controll);

        this._html_elements.title.click(function () {
            $(".portcontroller.customcontroll").removeClass("active");
            this._html_elements.custom_controll.addClass("active")
        }.bind(this))

    }

    remove(){
        this._html_representation.remove();
        if(all_boards[this.port] !== undefined)
            all_boards[this.port].remove();
        all_ports.splice(all_ports.indexOf(this),1);
        delete  this
    }

    set_available(){
        this._html_elements.activate_button.show();
        this._html_elements.deactivate_button.hide();
    }

    set_connected(){
        this._html_elements.activate_button.hide();
        this._html_elements.deactivate_button.show();
    }
    set_identified(){
        this._html_elements.activate_button.hide();
        this._html_elements.deactivate_button.show();
        boardcontroller_get_board_data(this.port);

    }

    set_ignored(){
        this._html_elements.activate_button.show();
        this._html_elements.deactivate_button.hide();
    }

    set_port_controller_div(portcontroller_div) {
        this.portcontroller_div = portcontroller_div;
        if (this.portcontroller_div == null) return;
        this.portcontroller_div.append(this._html_representation);

    }

}


class Board{
    constructor(port){
        console.log("new Board",port);
        this.port=port;
        this._create_html_representation();
        this.set_board_controller_div(board_controller_div);
        this.board_data={};
        this.set_title("Board on "+this.port);
    }

    _create_html_representation (){
        this._html_representation = board_controller_container.clone();
        this._html_elements={};
        this._html_elements.title = this._html_representation.find('[name="title"]');
        this._html_elements.form = this._html_representation.find('[name="form"]');
        this._html_elements.form.attr("onsubmit","return false;");
    }

    set_board_controller_div(board_controller_div) {
        this.board_controller_div = board_controller_div;
        if (this.board_controller_div == null) return;
        this.board_controller_div.append(this._html_representation);
    }

    set_title(title){
        this._html_elements.title.text(title)
    }

    update(board_data){
        this._html_elements.form.empty();
        if(board_data.arduino_variables !== undefined)
            for(let name in board_data.arduino_variables){
                let input=$(board_data.arduino_variables[name].form);

                this._html_elements.form.append('<label for="'+name+'">'+name+'</label>');
                this._html_elements.form.append(input);
                input.change(function () {
                    wscs.send(wscs.commandmessage("set_board_attribute","gui","server",true,[],{port:this.port,attribute:name,value:input.val(
                        )}))
                }.bind(this))
            }
    }

    remove(){
        this._html_representation.remove();
        delete all_boards[this.port];
        delete this
    }
}

function boardcontroller_get_board_data(port){
    wscs.send(wscs.commandmessage("get_board","gui","server",true,[],{port:port}));
}

function boardcontroller_set_ports(data){
    var ports = data.data.kwargs.connected_ports.concat(data.data.kwargs.available_ports).concat(data.data.kwargs.ignored_ports);
    ports =  ports.filter(function (item, pos) {return ports.indexOf(item) === pos});
    loop1:
        for(let i=0;i<ports.length;i++){
            for(let j=0;j<all_ports.length;j++){
                if(all_ports[j].port === ports[i]) {
                    if (data.data.kwargs.available_ports.indexOf(ports[i]) > -1) {
                        all_ports[j].set_available()
                    }
                    if (data.data.kwargs.connected_ports.indexOf(ports[i]) > -1) {
                        all_ports[j].set_connected()
                    }
                    if (data.data.kwargs.ignored_ports.indexOf(ports[i]) > -1) {
                        all_ports[j].set_ignored()
                    }
                    if (data.data.kwargs.identified_ports.indexOf(ports[i]) > -1) {
                        all_ports[j].set_identified()
                    }

                    continue loop1;
                }
            }
            let np = new Port(ports[i]);
            all_ports.push(np);
            if (data.data.kwargs.available_ports.indexOf(ports[i]) > -1) {
                np.set_available()
            }
            if (data.data.kwargs.connected_ports.indexOf(ports[i]) > -1) {
                np.set_connected()
            }
            if (data.data.kwargs.ignored_ports.indexOf(ports[i]) > -1) {
                np.set_ignored()
            }
            if (data.data.kwargs.identified_ports.indexOf(ports[i]) > -1) {
                np.set_identified()
            }
        }

    loop2:
        for(let i=all_ports.length-1;i>=0;i--){
            for(let j=0;j<ports.length;j++){
                if(ports[j] === all_ports[i].port)
                    continue loop2;
            }
            let removeport = all_ports[i];
            removeport.remove();
        }
}

function boardcontroller_set_board(data){
    let port = data.data.kwargs.port;
    let board_data = data.data.kwargs.board;
    if(all_boards[port] === undefined)
        all_boards[port]=new Board(port);
    all_boards[port].update(board_data);
}

function boardcontroller_onidentify(){
    wscs.send(wscs.commandmessage("get_ports","gui","server"))
}

wscs.add_on_indentify_function(boardcontroller_onidentify);
wscs.add_cmd_funcion("set_ports",boardcontroller_set_ports);
wscs.add_cmd_funcion("port_closed",function (){setTimeout(boardcontroller_onidentify,1000);});
wscs.add_cmd_funcion("port_opened",function (){setTimeout(boardcontroller_onidentify,1000);});

wscs.add_cmd_funcion("set_board",boardcontroller_set_board);