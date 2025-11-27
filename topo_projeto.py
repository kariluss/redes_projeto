from mininet.topo import Topo

class TopoProjeto(Topo):
    def build(self):
        # switches
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        s3 = self.addSwitch("s3")
        
        # hosts
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")

        # links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)

        self.addLink(s1, s2, delay="10ms", bw=100)
        self.addLink(s2, s3, delay="15ms", bw=100)

topos = {"topoprojeto": (lambda: TopoProjeto())}
