import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

const Assets = () => {
  return (
    <NavDropdown title="Activos" id="collapsible-nav-dropdown">
      <NavDropdown.Item href="/assets/create">
        Crear Activo
      </NavDropdown.Item>
      <NavDropdown.Item href="/assets/info">
        Informacion de Activos
      </NavDropdown.Item>
      <NavDropdown.Item href="/assets">
        Listar Activos de una cuenta
      </NavDropdown.Item>
      <NavDropdown.Divider />
      <NavDropdown.Item href="/assets/add">
        Agregar cantidad a un Activo
      </NavDropdown.Item>
      <NavDropdown.Item href="/assets/sub">
        Eliminar cantidad de un Activo
      </NavDropdown.Item>
    </NavDropdown>
  )
}

const Navigation = () => {
  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary" data-bs-theme="dark">
      <Container>
        <Navbar.Brand href="/">Iroha DApp</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Assets />
            {/* <Nav.Link href="#features">Features</Nav.Link>
            <Nav.Link href="#pricing">Pricing</Nav.Link> */}
          </Nav>
          {/* <Nav>
            <Nav.Link href="#deets">More deets</Nav.Link>
            <Nav.Link eventKey={2} href="#memes">
              Dank memes
            </Nav.Link>
          </Nav> */}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;